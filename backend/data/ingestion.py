from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

DEFAULT_DOWNLOAD_DIR = Path(r"C:\Users\ajayk\Downloads")


@dataclass
class DatasetBundle:
    transactions: pd.DataFrame
    identity: pd.DataFrame
    closed_cases_history: pd.DataFrame
    case_pack: pd.DataFrame


def find_dataset_files(base_dir: str | Path | None = None) -> List[Path]:
    root = Path(base_dir) if base_dir is not None else DEFAULT_DOWNLOAD_DIR
    if not root.exists():
        return []

    target_names = {
        "transactions.csv",
        "identity.csv",
        "closed_cases_history.csv",
        "case_pack.csv",
    }

    matches = []
    for path in root.iterdir():
        if path.is_file() and path.name in target_names:
            matches.append(path)
    return sorted(matches)


def load_real_dataset_bundle(base_dir: str | Path | None = None) -> DatasetBundle:
    files = find_dataset_files(base_dir)
    file_map = {path.name: path for path in files}

    required = [
        "transactions.csv",
        "identity.csv",
        "closed_cases_history.csv",
        "case_pack.csv",
    ]
    missing = [name for name in required if name not in file_map]
    if missing:
        raise FileNotFoundError(f"Missing dataset files: {missing}")

    transactions = pd.read_csv(file_map["transactions.csv"])
    identity = pd.read_csv(file_map["identity.csv"])
    closed_cases_history = pd.read_csv(file_map["closed_cases_history.csv"])
    case_pack = pd.read_csv(file_map["case_pack.csv"])

    return DatasetBundle(
        transactions=transactions,
        identity=identity,
        closed_cases_history=closed_cases_history,
        case_pack=case_pack,
    )


def infer_entity_mapping() -> Dict[str, str]:
    bundle = load_real_dataset_bundle()
    tx = bundle.transactions
    identity = bundle.identity
    case_pack = bundle.case_pack

    mapping = {
        "transaction_id": "TransactionID",
        "customer_id": "customer_id" if "customer_id" in tx.columns else "customer_id",
        "device_id": "DeviceInfo" if "DeviceInfo" in identity.columns else "device_id",
        "risk_score": "risk_score" if "risk_score" in tx.columns else "risk_score",
        "case_id": "case_id" if "case_id" in case_pack.columns else "case_id",
        "trigger_id": "flagged_txn_id" if "flagged_txn_id" in case_pack.columns else "flagged_txn_id",
    }
    return mapping


def _json_safe(value: Any) -> Any:
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and pd.isna(value):
            return None
        return value

    if isinstance(value, dict):
        return {str(key): _json_safe(val) for key, val in value.items()}

    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]

    if hasattr(value, "dtype") and hasattr(value, "tolist"):
        try:
            return _json_safe(value.tolist())
        except TypeError:
            pass

    if hasattr(value, "item"):
        try:
            item = value.item()
            if isinstance(item, (list, tuple, dict)):
                return _json_safe(item)
            if item is None or (isinstance(item, float) and pd.isna(item)):
                return None
            return item
        except (TypeError, ValueError):
            pass

    return value


def build_graph_context(bundle: DatasetBundle, transaction_id: int | str) -> Dict[str, Any]:
    tx_df = bundle.transactions
    identity_df = bundle.identity
    history_df = bundle.closed_cases_history
    case_pack_df = bundle.case_pack

    tx_id = str(transaction_id).strip()
    tx_matches = tx_df[tx_df["TransactionID"].astype(str).str.strip() == tx_id]
    if tx_matches.empty:
        try:
            tx_matches = tx_df[tx_df["TransactionID"].astype(str).str.strip() == str(int(float(tx_id)))]
        except (TypeError, ValueError):
            tx_matches = tx_df.iloc[0:0]

    transaction = tx_matches.iloc[0].to_dict() if not tx_matches.empty else {}
    transaction = _json_safe(transaction)
    customer_id = transaction.get("customer_id")

    match_context = {}
    if not identity_df.empty:
        id_matches = identity_df[identity_df["TransactionID"].astype(str).str.strip() == tx_id]
        if id_matches.empty:
            try:
                id_matches = identity_df[identity_df["TransactionID"].astype(str).str.strip() == str(int(float(tx_id)))]
            except (TypeError, ValueError):
                id_matches = identity_df.iloc[0:0]
        if not id_matches.empty:
            match_context = _json_safe(id_matches.iloc[0].to_dict())

    history = []
    if customer_id:
        customer_matches = history_df[history_df["customer_id"].astype(str).str.strip() == str(customer_id).strip()]
        history = _json_safe(customer_matches.head(5).to_dict(orient="records"))

    case_matches = []
    if not case_pack_df.empty:
        case_matches_df = case_pack_df[case_pack_df["flagged_txn_id"].astype(str).str.strip() == tx_id]
        if case_matches_df.empty:
            try:
                case_matches_df = case_pack_df[case_pack_df["flagged_txn_id"].astype(str).str.strip() == str(int(float(tx_id)))]
            except (TypeError, ValueError):
                case_matches_df = case_pack_df.iloc[0:0]
        case_matches = _json_safe(case_matches_df.to_dict(orient="records"))

    return {
        "transaction": transaction,
        "customer_id": customer_id,
        "match_context": match_context,
        "history": history,
        "case_matches": case_matches,
    }
