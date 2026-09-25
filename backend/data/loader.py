from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import pandas as pd


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def find_data_files(data_dir: str | Path | None = None) -> List[Path]:
    """Return candidate data files for HHGOA ingestion.

    The exact dataset files are not present in the current workspace, so this
    function scans the project data directory for CSV/XLSX files and leaves the
    specific mapping to the real dataset columns to be confirmed once the files are added.
    """
    base_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    if not base_dir.exists():
        return []
    patterns = ["*.csv", "*.CSV", "*.xlsx", "*.xls"]
    files: List[Path] = []
    for pattern in patterns:
        files.extend(base_dir.glob(pattern))
    return sorted({path for path in files})


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """Load a dataset file into a pandas DataFrame."""
    path = Path(file_path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported dataset format: {path.suffix}")
