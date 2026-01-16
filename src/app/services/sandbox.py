import os
import subprocess
import sys
from pathlib import Path
from typing import Optional
from uuid import uuid4

from .storage import ensure_dir, sanitize_filename


def _scripts_dir(sandbox_dir: str) -> Path:
    return ensure_dir(sandbox_dir) / "_scripts"


def _build_sandbox_path(sandbox_dir: str, filename: str) -> Path:
    base_dir = ensure_dir(sandbox_dir)
    safe_name = sanitize_filename(filename)
    return base_dir / safe_name


def _build_script_path(sandbox_dir: str, filename: str) -> Path:
    safe_name = sanitize_filename(filename)
    if not safe_name.endswith(".py"):
        safe_name += ".py"
    scripts_dir = _scripts_dir(sandbox_dir)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    return scripts_dir / safe_name


def _write_script(sandbox_dir: str, filename: Optional[str], code: str) -> Path:
    safe_name = filename or f"script_{uuid4().hex}.py"
    file_path = _build_script_path(sandbox_dir, safe_name)
    file_path.write_text(code, encoding="utf-8")
    return file_path


def run_python_script(
    sandbox_dir: str,
    code: str,
    filename: Optional[str] = None,
    timeout_seconds: int = 5,
    max_output_chars: int = 10_000,
) -> dict:
    if filename:
        data_path = _build_sandbox_path(sandbox_dir, filename)
        if not data_path.exists():
            missing_name = data_path.name
            return {
                "filename": missing_name,
                "exit_code": 1,
                "stdout": "",
                "stderr": f'文件不存在: "{missing_name}"',
            }

    script_path = _write_script(sandbox_dir, None, code)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(Path(sandbox_dir).resolve()),
        env=env,
        timeout=timeout_seconds,
    )

    stdout = (result.stdout or "")[:max_output_chars]
    stderr = (result.stderr or "")[:max_output_chars]

    return {
        "filename": script_path.name,
        "exit_code": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
