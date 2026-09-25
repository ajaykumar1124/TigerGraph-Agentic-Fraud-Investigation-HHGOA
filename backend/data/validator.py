from __future__ import annotations

from typing import Iterable, List

import pandas as pd


def validate_required_columns(df: pd.DataFrame, required: Iterable[str]) -> List[str]:
    """Return missing required columns for the current dataset."""
    required_columns = set(required)
    actual_columns = set(df.columns)
    return sorted(required_columns - actual_columns)
