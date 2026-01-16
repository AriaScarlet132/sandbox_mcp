import os
import signal
import subprocess
import sys
import time

from .config import settings


def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    return env


def main() -> int:
    env = _build_env()

    rest_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        settings.rest_host,
        "--port",
        str(settings.rest_port),
    ]

    mcp_cmd = [
        sys.executable,
        "-m",
        "app.mcp_server",
    ]

    rest_proc = subprocess.Popen(rest_cmd, env=env)
    mcp_proc = subprocess.Popen(mcp_cmd, env=env)

    def shutdown(signum: int, _frame) -> None:
        for proc in (rest_proc, mcp_proc):
            try:
                proc.terminate()
            except Exception:
                pass

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        rest_code = rest_proc.poll()
        mcp_code = mcp_proc.poll()
        if rest_code is not None or mcp_code is not None:
            shutdown(signal.SIGTERM, None)
            time.sleep(0.2)
            return rest_code if rest_code is not None else (mcp_code or 0)
        time.sleep(0.2)


if __name__ == "__main__":
    raise SystemExit(main())
