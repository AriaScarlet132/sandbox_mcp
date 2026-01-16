import json
import logging
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .config import settings
from .services.sandbox import run_python_script
from .services.springboot_client import fetch_data as springboot_fetch_data
from .main import _dataframe_head_to_markdown, _markdown_to_dataframe
from .services.storage import (
    build_parquet_filename,
    save_dataframe_parquet,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("mcp")

mcp = FastMCP("agent-data-bridge", host="0.0.0.0", port=9000)


@mcp.tool()
async def fetch_data(host: str, userid: str, sql: str, dataset: str) -> str:
    """
    根据 SQL 拉取数据，并返回可读摘要（小数据直接表格，大数据落盘到沙盒数据区）。

    行为：
    - Rows ≤ 15：直接返回完整 Markdown 表格。
    - Rows > 15：将结果保存为 parquet 到沙盒数据目录（settings.sandbox_dir），并返回字段预览 + 前 5 行。

    说明：
    - 保存后的 parquet 文件可在 `sandbox_run` 中用 pandas 读取，例如：`pd.read_parquet("<file_name>")`。

    参数：
    - host: 服务地址，例如 http://192.168.10.21:3000
    - userid: 业务用户标识
    - sql: 待执行的 SQL 语句
    - dataset: 数据集名称（用于生成更可读的 parquet 文件名）
    """
    logger.info(
        "调用工具: fetch_data 参数=%s",
        json.dumps(
            {"host": host, "userid": userid, "sql": sql, "dataset": dataset},
            ensure_ascii=False,
        ),
    )
    raw = await springboot_fetch_data(host, userid, sql, dataset)
    markdown = ((raw or {}).get("data") or {}).get("markdown")
    if not markdown:
        logger.warning("fetch_data 未获取到 markdown 数据")
        return "未获取到有效的 markdown 结果。"

    df = _markdown_to_dataframe(markdown)
    row_count = len(df)

    if row_count <= 15:
        logger.info("fetch_data 返回小数据集 Rows=%s", row_count)
        return "\n".join(
            [
                "SQL 执行成功。",
                f"数据量较小 (Rows: {row_count})，直接返回：",
                markdown.strip(),
            ]
        )

    file_name = build_parquet_filename(dataset)
    save_dataframe_parquet(settings.sandbox_dir, df, file_name)
    logger.info("fetch_data 保存 parquet 文件=%s Rows=%s", file_name, row_count)

    fields_preview = "\n".join(
        [f"- {col} ({dtype})" for col, dtype in df.dtypes.items()]
    )
    head_preview = _dataframe_head_to_markdown(df, 5)

    return "\n".join(
        [
            "SQL 执行成功。",
            f"由于数据量较大 (Rows: {row_count})，数据已保存至沙盒文件系统。",
            f'文件名： "{file_name}" (位于 settings.sandbox_dir)',
            "字段预览：",
            fields_preview,
            "数据前5行摘要：",
            head_preview,
            "[... 仅展示前5行 ...]",
            "提示：可使用 sandbox_run 执行 Python 代码读取该文件，例如：",
            '  import pandas as pd\n  df = pd.read_parquet("%s")\n  print(df.head())'
            % file_name,
        ]
    )


@mcp.tool()
async def sandbox_run(code: str, filename: Optional[str] = None) -> dict:
    """
    在沙盒目录中执行 Python 代码（可读写沙盒数据目录中的文件，例如 fetch_data 生成的 parquet）。

    运行环境：
    - 代码的工作目录为 settings.sandbox_dir。
    - 预装依赖：pandas、numpy、pyarrow。
    - 服务器会将脚本临时文件写入 settings.sandbox_dir/_scripts/（避免污染数据目录）。

    参数：
    - code: 要执行的 Python 代码文本。
    - filename: （可选）仅用于“存在性预检查”的沙盒数据文件名；用于在执行前快速失败并返回明确错误。

    返回：
    - dict：包含 filename(实际生成的脚本名)、exit_code、stdout、stderr。
    """
    code_preview = (code or "")[:500]
    logger.info(
        "调用工具: sandbox_run 参数=%s",
        json.dumps(
            {
                "filename": filename,
                "code_length": len(code or ""),
                "code_preview": code_preview,
            },
            ensure_ascii=False,
        ),
    )
    result = run_python_script(
        settings.sandbox_dir,
        code,
        filename=filename,
        timeout_seconds=settings.sandbox_timeout_seconds,
        max_output_chars=settings.sandbox_max_output_chars,
    )
    logger.info(
        "sandbox_run 执行完成 filename=%s exit_code=%s stdout_len=%s stderr_len=%s",
        result.get("filename"),
        result.get("exit_code"),
        len(result.get("stdout") or ""),
        len(result.get("stderr") or ""),
    )
    exit_code = result.get("exit_code")
    stdout_text = (result.get("stdout") or "")[:2000]
    stderr_text = (result.get("stderr") or "")[:2000]
    if exit_code and exit_code != 0:
        logger.error(
            "sandbox_run 非零退出 code=%s; stderr=%s; stdout=%s",
            exit_code,
            stderr_text,
            stdout_text,
        )
    else:
        logger.debug("sandbox_run stdout_preview=%s", stdout_text)

    return result


@mcp.tool()
async def sandbox_list_files() -> str:
    """
    列出沙盒数据目录（settings.sandbox_dir）根目录下的所有文件。

    说明：
    - 只列出根目录文件；不会遍历嵌套目录。
    - 会忽略内部脚本目录 `settings.sandbox_dir/_scripts/` 以及任何子目录。
    - 返回包含文件名与大小（字节），按修改时间倒序。
    """
    base_dir = Path(settings.sandbox_dir).resolve()
    if not base_dir.exists():
        return "沙盒数据目录不存在。"

    entries: list[tuple[float, str]] = []
    for path in base_dir.iterdir():
        # 不用管嵌套目录：只展示根目录的文件
        if not path.is_file():
            continue
        if path.name == "_scripts":
            continue
        stat = path.stat()
        entries.append((stat.st_mtime, f"- {path.name} ({stat.st_size} bytes)"))

    if not entries:
        return "未找到匹配文件。"

    entries.sort(key=lambda x: x[0], reverse=True)
    lines = ["沙盒数据目录文件列表："] + [line for _, line in entries]
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="sse")
