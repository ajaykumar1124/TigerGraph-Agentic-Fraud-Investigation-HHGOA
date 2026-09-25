"""TigerGraph-backed investigation tools used by the LLM agent."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.data.ingestion import build_graph_context, load_real_dataset_bundle


def get_transaction(txn_id: str) -> Dict[str, Any]:
    """Return transaction-level evidence for a given ID."""
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, txn_id)
        return {"success": True, "transaction": context.get("transaction", {}), "customer_id": context.get("transaction", {}).get("customer_id")}
    except Exception as exc:  # pragma: no cover - defensive fallback
        return {"success": False, "error": str(exc)}


def get_customer_history(customer_id: str) -> Dict[str, Any]:
    """Return historical activity for a customer."""
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, customer_id)
        return {"success": True, "history": context.get("history", []), "customer_id": customer_id}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_device_connections(device_id: Optional[str]) -> Dict[str, Any]:
    """Return device-linked transaction and customer context."""
    if not device_id:
        return {"success": True, "connections": []}
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, device_id)
        return {"success": True, "connections": context.get("match_context", {}).get("device_connections", []), "device_id": device_id}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_ip_connections(ip_address: Optional[str]) -> Dict[str, Any]:
    """Return IP-linked network context."""
    if not ip_address:
        return {"success": True, "connections": []}
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, ip_address)
        return {"success": True, "connections": context.get("match_context", {}).get("ip_connections", []), "ip_address": ip_address}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_related_transactions(customer_id: str) -> Dict[str, Any]:
    """Return transaction relationships around a customer."""
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, customer_id)
        return {"success": True, "related_transactions": context.get("case_matches", []) or context.get("history", []), "customer_id": customer_id}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def get_historical_cases(customer_id: str) -> Dict[str, Any]:
    """Return historical case patterns."""
    try:
        bundle = load_real_dataset_bundle()
        context = build_graph_context(bundle, customer_id)
        return {"success": True, "historical_cases": context.get("history", []), "customer_id": customer_id}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


ALL_TOOLS = {
    "get_transaction": get_transaction,
    "get_customer_history": get_customer_history,
    "get_device_connections": get_device_connections,
    "get_ip_connections": get_ip_connections,
    "get_related_transactions": get_related_transactions,
    "get_historical_cases": get_historical_cases,
}
