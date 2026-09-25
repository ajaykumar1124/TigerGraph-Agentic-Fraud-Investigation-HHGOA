from __future__ import annotations

from typing import Dict, List

import pandas as pd


def infer_entity_columns(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Return the likely entity-related columns.

    The exact mapping depends on the actual HHGOA files and README. This helper
    is a placeholder for the real column discovery work once the dataset is added.
    """
    columns = list(df.columns)
    return {
        "transaction_id_candidates": [c for c in columns if "id" in c.lower() or "txn" in c.lower()],
        "customer_candidates": [c for c in columns if "customer" in c.lower() or "client" in c.lower()],
        "account_candidates": [c for c in columns if "account" in c.lower() or "card" in c.lower()],
        "device_candidates": [c for c in columns if "device" in c.lower() or "ip" in c.lower()],
        "risk_candidates": [c for c in columns if "risk" in c.lower() or "score" in c.lower()],
    }
