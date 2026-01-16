from typing import Optional

import re

import subprocess
from fastapi import FastAPI, HTTPException, Request, UploadFile
from pydantic import BaseModel

import pandas as pd

from .config import settings
from .services.sandbox import run_python_script
from .services.springboot_client import fetch_data as springboot_fetch_data
from .services.storage import build_parquet_filename, save_dataframe_parquet

app = FastAPI(title="Agent Data Bridge", version="0.1.0")


class FetchRequest(BaseModel):
    host: str
    userid: str
    sql: str
    dataset: str


class FetchResponse(BaseModel):
    message: str


class SandboxRequest(BaseModel):
    filename: Optional[str] = None
    code: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/api/fetch", response_model=FetchResponse)
async def fetch_data(request: FetchRequest) -> FetchResponse:
    try:
        raw = await springboot_fetch_data(
            request.host,
            request.userid,
            request.sql,
            request.dataset,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"fetch failed: {exc}")

    markdown = ((raw or {}).get("data") or {}).get("markdown")
    if not markdown:
        raise HTTPException(status_code=502, detail="missing markdown in response")

    df = _markdown_to_dataframe(markdown)
    row_count = len(df)

    if row_count <= 15:
        message = "\n".join(
            [
                "SQL 执行成功。",
                f"数据量较小 (Rows: {row_count})，直接返回：",
                markdown.strip(),
            ]
        )
        return FetchResponse(message=message)

    file_name = build_parquet_filename(request.dataset)
    save_dataframe_parquet(settings.sandbox_dir, df, file_name)

    fields_preview = "\n".join(
        [f"- {col} ({dtype})" for col, dtype in df.dtypes.items()]
    )
    head_preview = _dataframe_head_to_markdown(df, 5)

    message = "\n".join(
        [
            "SQL 执行成功。",
            f"由于数据量较大 (Rows: {row_count})，数据已保存至沙盒文件系统。",
            f'文件名： "{file_name}"',
            "字段预览：",
            fields_preview,
            "数据前5行摘要：",
            head_preview,
            "[... 仅展示前5行 ...]",
        ]
    )
    return FetchResponse(message=message)


def _markdown_to_dataframe(markdown: str) -> pd.DataFrame:
    """Parse the first Markdown table in text into a DataFrame.

    This is intentionally tolerant to common variants:
    - Optional leading/trailing pipes
    - Alignment markers in the separator row (e.g. :---:)
    - Extra text above/below the table
    """

    def is_separator_line(line: str) -> bool:
        # Examples:
        # |---|---|
        # |:---|---:|
        # ---|---
        return bool(
            re.match(
                r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$",
                line,
            )
        )

    def split_row(line: str) -> list[str]:
        return [part.strip() for part in line.strip().strip("|").split("|")]

    raw_lines = [ln.rstrip("\n") for ln in (markdown or "").splitlines()]
    if len(raw_lines) < 2:
        return pd.DataFrame()

    table_start: int | None = None
    for i in range(len(raw_lines) - 1):
        header_line = raw_lines[i].strip()
        sep_line = raw_lines[i + 1].strip()
        if not header_line or not sep_line:
            continue
        if "|" not in header_line:
            continue
        if is_separator_line(header_line):
            continue
        if is_separator_line(sep_line):
            table_start = i
            break

    if table_start is None:
        return pd.DataFrame()

    header = split_row(raw_lines[table_start])
    if not header:
        return pd.DataFrame()

    col_count = len(header)
    rows: list[list[str]] = []
    for line in raw_lines[table_start + 2 :]:
        stripped = line.strip()
        if not stripped:
            break
        if "|" not in stripped:
            break
        if is_separator_line(stripped):
            continue

        parts = split_row(stripped)
        if len(parts) < col_count:
            parts = parts + [""] * (col_count - len(parts))
        elif len(parts) > col_count:
            parts = parts[:col_count]
        rows.append(parts)

    return pd.DataFrame(rows, columns=header)


def _dataframe_head_to_markdown(df: pd.DataFrame, n: int) -> str:
    head = df.head(n)
    if head.empty:
        return "(无可预览数据)"
    columns = [str(col) for col in head.columns]
    sep = ["---" for _ in columns]
    rows = [columns, sep]
    for _, row in head.iterrows():
        rows.append(["" if pd.isna(v) else str(v) for v in row.tolist()])
    return "\n".join(["|" + "|".join(r) + "|" for r in rows])


@app.post("/api/sandbox/run")
async def run_sandbox(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")

    code: Optional[str] = None
    filename: Optional[str] = None

    if "multipart/form-data" in content_type:
        form = await request.form()
        upload = form.get("file")
        if isinstance(upload, UploadFile):
            code = (await upload.read()).decode("utf-8")
            filename = upload.filename
        else:
            code = form.get("code")
            filename = form.get("filename")
    else:
        data = await request.json()
        parsed = SandboxRequest(**data)
        code = parsed.code
        filename = parsed.filename

    if not code:
        raise HTTPException(status_code=400, detail="Provide code or file")

    try:
        return run_python_script(
            settings.sandbox_dir,
            code,
            filename=filename,
            timeout_seconds=settings.sandbox_timeout_seconds,
            max_output_chars=settings.sandbox_max_output_chars,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Execution timed out")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
