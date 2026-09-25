from __future__ import annotations

from typing import Iterable

import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize the incoming HHGOA data to a clean tabular form.

    This function deliberately keeps the cleaning rules generic; the exact column
    names must be confirmed from the real dataset files before production use.
    """
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]
    cleaned = cleaned.replace({"\r\n": " ", "\n": " "}, regex=True)
    cleaned = cleaned.dropna(how="all")
    return cleaned
