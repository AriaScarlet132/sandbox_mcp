from pathlib import Path

from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # REST (FastAPI) 服务监听地址
    rest_host: str = "0.0.0.0"
    rest_port: int = 8000

    # MCP (SSE Transport) 服务监听地址
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 9000

    # Spring Boot OAuth2 client credentials（用于获取 access_token）
    app_id: str = "agent"
    app_secret: str = "agent"

    spring_boot_base_url: str = "http://localhost:8080"
    spring_boot_api_path: str = "/api/query"
    # 默认路径固定为“项目根目录”下的目录，避免受进程 cwd 影响（例如从 src/ 启动时）。
    data_dir: str = str(PROJECT_ROOT / "data")
    sandbox_dir: str = str(PROJECT_ROOT / "sandbox_storage")
    sandbox_timeout_seconds: int = 5
    sandbox_max_output_chars: int = 10_000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
