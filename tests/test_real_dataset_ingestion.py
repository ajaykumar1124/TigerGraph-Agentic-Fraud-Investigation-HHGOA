from pathlib import Path

from backend.data.ingestion import (
    build_graph_context,
    find_dataset_files,
    infer_entity_mapping,
    load_real_dataset_bundle,
)


def test_find_dataset_files_finds_real_downloads():
    files = find_dataset_files()
    names = {path.name for path in files}
    assert {"transactions.csv", "identity.csv", "closed_cases_history.csv", "case_pack.csv"}.issubset(names)


def test_infer_entity_mapping_uses_real_dataset_columns():
    mapping = infer_entity_mapping()
    assert "transaction_id" in mapping
    assert "customer_id" in mapping
    assert "device_id" in mapping
    assert "risk_score" in mapping
    assert mapping["transaction_id"] == "TransactionID"


def test_build_graph_context_returns_transaction_related_summary():
    bundle = load_real_dataset_bundle()
    context = build_graph_context(bundle, transaction_id="TX00000001")
    assert context["transaction"]["TransactionID"] == "TX00000001"
    assert context["transaction"]["customer_id"] == "C000103"
    assert "match_context" in context
    assert "history" in context
