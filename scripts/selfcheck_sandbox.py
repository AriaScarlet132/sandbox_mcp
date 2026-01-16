from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from app.config import settings
from app.services.sandbox import run_python_script
from app.services.storage import save_dataframe_parquet


def main() -> None:
    os.makedirs(settings.sandbox_dir, exist_ok=True)

    parquet_name = "demo_test.parquet"
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    save_dataframe_parquet(settings.sandbox_dir, df, parquet_name)

    code = (
        "import pandas as pd\n"
        f"df = pd.read_parquet('{parquet_name}')\n"
        "print(df.head().to_string(index=False))\n"
    )
    result = run_python_script(settings.sandbox_dir, code, filename=parquet_name)

    print("sandbox_dir:", settings.sandbox_dir)
    print("script_file:", result.get("filename"))
    print("exit_code:", result.get("exit_code"))
    print("stdout:\n", result.get("stdout"))
    print("stderr:\n", result.get("stderr"))


if __name__ == "__main__":
    main()
