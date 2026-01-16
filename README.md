# Agent Data Bridge

一个面向 Agent 的“数据桥接 + 轻量沙盒执行”服务，提供两种对外形态：

- FastAPI HTTP API：用于手工/系统直接调用。
- MCP Server（SSE Transport）：把能力以 Tool 的形式暴露给支持 MCP 的客户端。

目前实际实现包含：

- 通过两步 OAuth2（token -> query）调用 Spring Boot 接口获取数据（见 [src/app/services/springboot_client.py](src/app/services/springboot_client.py)）。
- 将返回结果中的首个 Markdown 表格解析为 DataFrame；小数据直接返回表格，大数据保存为 parquet 到沙盒目录并返回摘要（见 [src/app/main.py](src/app/main.py)）。
- 提供一个简易 Python “沙盒执行”入口：在指定的沙盒目录中运行脚本，支持超时与输出长度截断（见 [src/app/services/sandbox.py](src/app/services/sandbox.py)）。

## 运行要求

- Python >= 3.12
- 推荐使用 uv 管理依赖（见 [pyproject.toml](pyproject.toml)）

## 快速开始

1. 安装依赖


- `uv sync`

1. 启动 HTTP API（FastAPI）

- `uv run -- uvicorn app.main:app --reload --app-dir src`

默认监听 `http://127.0.0.1:8000`。

如果希望“一条命令同时启动 REST + MCP”，可使用：

- `uv run -- python -m app.run_all`

1.（可选）启动 MCP Server（SSE）

本项目的 MCP Server 默认监听 `0.0.0.0:9000`（可通过 `MCP_HOST`/`MCP_PORT` 修改），并使用 SSE 传输：

- SSE 端点：`GET /sse`
- 消息端点：`POST /messages/`

启动命令：

- Windows（PowerShell，推荐）：

```powershell
$env:PYTHONPATH = "src"
uv run -- python -m app.mcp_server
```

- 或者切换到 `src` 目录运行（一次性）：

```powershell
pushd src
uv run -- python -m app.mcp_server
popd
```

- macOS/Linux：

```bash
PYTHONPATH=src uv run -- python -m app.mcp_server
```

## 配置（.env）

复制 [\.env.example](.env.example) 为 `.env` 后按需修改。

当前代码实际会用到的配置（与 [.env.example](.env.example) 保持一致）：

- `REST_HOST` / `REST_PORT`：REST(FastAPI) 监听地址（用于 Docker 启动与一键启动脚本）。
- `MCP_HOST` / `MCP_PORT`：MCP(SSE) 监听地址。
- `APP_ID` / `APP_SECRET`：Spring Boot OAuth2 client credentials（默认 `agent/agent`）。

说明：

- `SPRING_BOOT_BASE_URL` / `SPRING_BOOT_API_PATH` 目前在代码中未被使用；`/api/fetch` 与 MCP 的 `fetch_data` 都会直接使用传入的 `host` 参数作为目标地址（见 [src/app/services/springboot_client.py](src/app/services/springboot_client.py)）。

## HTTP API

### 健康检查

- `GET /health`

返回：`{"status":"ok"}`

### 拉取数据并返回摘要

- `POST /api/fetch`

请求体：

```json
{
  "host": "http://192.168.10.21:3000",
  "userid": "Admin",
  "sql": "select ...",
  "dataset": "demo"
}
```

行为（与实现一致，见 [src/app/main.py](src/app/main.py)）：

- 解析返回结果中的 `data.markdown`（Markdown 表格）。
- `Rows <= 15`：直接返回完整 Markdown 表格。
- `Rows > 15`：保存为 parquet 到 `SANDBOX_DIR`，并返回字段预览 + 前 5 行。

响应：

```json
{ "message": "..." }
```

示例（curl）：

```bash
curl -X POST http://127.0.0.1:8000/api/fetch \
  -H "Content-Type: application/json" \
  -d '{"host":"http://192.168.10.21:3000","userid":"Admin","sql":"select 1","dataset":"demo"}'
```

### 运行沙盒脚本

- `POST /api/sandbox/run`

方式 A：JSON

```json
{ "filename": "anything.py", "code": "print(123)" }
```

方式 B：multipart/form-data

- 上传字段名 `file`（.py 文件）
- 或者传 `code` / `filename`

返回（与实现一致，见 [src/app/services/sandbox.py](src/app/services/sandbox.py)）：

```json
{
  "filename": "script_xxx.py",
  "exit_code": 0,
  "stdout": "...",
  "stderr": "..."
}
```

## MCP Tools

MCP Server 目前提供以下 tools（见 [src/app/mcp_server.py](src/app/mcp_server.py)）：

- `fetch_data(host, userid, sql, dataset) -> str`
- `sandbox_run(code, filename=None) -> dict`
- `sandbox_list_files() -> str`

常见用法：先 `fetch_data` 生成 parquet 文件名，再用 `sandbox_run` 执行 Python 读取：

```python
import pandas as pd
df = pd.read_parquet("<file_name>")
print(df.head())
```

## 目录说明

- `sandbox_storage/`：默认沙盒数据目录（可通过 `SANDBOX_DIR` 覆盖）。
- `sandbox_storage/_scripts/`：沙盒执行时写入的临时脚本目录（自动创建）。

## 安全与限制

- 沙盒执行不是强隔离：只是把工作目录固定到 `SANDBOX_DIR`，并加了超时与输出截断；请勿在不可信输入场景直接暴露到公网。
- Spring Boot 的 `client_id/client_secret` 已改为从 `.env` 读取（`APP_ID`/`APP_SECRET`，默认 `agent/agent`）。

## Docker

同时启动 REST + MCP（推荐使用 compose，并把沙盒目录挂载到宿主机）：

```bash
docker compose up --build
```

端口：

- REST: `http://127.0.0.1:${REST_PORT:-8000}`
- MCP(SSE): `http://127.0.0.1:${MCP_PORT:-9000}/sse`

数据卷：

- `./sandbox_storage` -> `/app/sandbox_storage`

## 常见问题

### Windows 下 `ModuleNotFoundError: No module named 'app'`

使用 PowerShell 运行 MCP Server 时，请先设置：

```powershell
$env:PYTHONPATH = "src"
uv run -- python -m app.mcp_server
```
