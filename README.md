# Agent Data Bridge

这是一个使用 FastAPI + uv (Python 3.12) 的中间层服务，用于：

- 由 Agent 触发调用 Spring Boot 获取数据（此处保留占位函数）
- 将结果保存为文件并返回摘要
- 提供一个简易 Python 沙盒执行入口（接收脚本内容或 .py 文件）

## 快速开始

1. 创建虚拟环境并安装依赖：
   - 使用 uv
     - `uv venv`
     - `uv sync`

2. 启动服务：
   - `uv run -- uvicorn app.main:app --reload --app-dir src`

3. 环境变量：
   - 复制 `.env.example` 为 `.env` 并按需修改

## API

- `POST /api/fetch`
  - 请求体：`{ "host": "http://192.168.10.21:3000", "userid": "Admin", "sql": "...", "dataset": "..." }`
  - 行为：调用 Spring Boot 获取数据 → 解析 markdown 表格 → 小数据直接返回，大数据保存为 parquet 并返回文本摘要

- `POST /api/sandbox/run`
  - 方式一：JSON
    - `{ "filename": "script.py", "code": "print(123)" }`
  - 方式二：multipart 表单上传 `.py` 文件

- `GET /health`

## 说明

- Spring Boot 调用逻辑在 `src/app/services/springboot_client.py` 中，已实现 token + 查询两步流程。
- 沙盒执行不是真正的安全隔离，仅提供超时与输出长度限制。生产环境建议使用容器或更严格的隔离方案。

## MCP

已提供 MCP 工具服务：

- `fetch_data(host, userid, sql, dataset)`
- `sandbox_run(code, filename=None)`

启动命令（需设置 PYTHONPATH）：
- `PYTHONPATH=src uv run -- python -m app.mcp_server`

默认端口：9000（Streamable HTTP，路径：/mcp）

**Windows 启动说明**

在 Windows（PowerShell）中直接运行 `uv run -- python -m app.mcp_server` 可能会遇到错误：

```
.venv\Scripts\python.exe: Error while finding module specification for 'app.mcp_server' (ModuleNotFoundError: No module named 'app')
```

这是因为默认情况下项目根目录下的 `src` 目录并不在 `PYTHONPATH` 中。可用以下两种简单方法在 Windows 下启动 MCP 服务：

- 临时设置会话环境变量（PowerShell）：

  ```powershell
  $env:PYTHONPATH = "src"
  uv run -- python -m app.mcp_server
  ```

- 切换到 `src` 目录再运行（适用于一次性运行）：

  ```powershell
  pushd src
  uv run -- python -m app.mcp_server
  popd
  ```

另外，如果你通过 `uvicorn` 启动并希望指出应用目录，可以使用 `--app-dir`：

```powershell
uv run -- uvicorn app.main:app --reload --app-dir src
```

说明：第一种方法把 `src` 加入当前 PowerShell 会话的 `PYTHONPATH`，第二种方法通过改变当前工作目录让 Python 能找到 `app` 包。两者任选其一即可解决 `ModuleNotFoundError` 问题。
