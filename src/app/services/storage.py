import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from uuid import uuid4


def ensure_dir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_payload(data_dir: str, payload: Any) -> str:
    data_path = ensure_dir(data_dir)
    file_name = (
        f"data_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid4().hex}.json"
    )
    file_path = data_path / file_name
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return file_name


def save_dataframe_parquet(data_dir: str, df: pd.DataFrame, file_name: str) -> str:
    data_path = ensure_dir(data_dir)
    file_path = data_path / file_name
    df.to_parquet(file_path, index=False)
    return file_name


def build_parquet_filename(dataset: str) -> str:
    safe_dataset = "".join(
        [c if c.isalnum() or c in ("-", "_") else "_" for c in dataset.strip()]
    )
    return f"df_{safe_dataset}_{uuid4().hex}.parquet"


def load_payload(data_dir: str, file_name: str) -> Any:
    file_path = Path(data_dir) / file_name
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(file_name: str) -> str:
    return os.path.basename(file_name)
