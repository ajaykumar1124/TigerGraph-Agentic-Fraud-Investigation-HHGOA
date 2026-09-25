"""LangGraph-friendly investigation state for the fraud agent."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class AgentState(TypedDict, total=False):
    """Minimal investigation state used by the agent and tool chain."""

    transaction_id: str
    customer_id: Optional[str]
    risk_score: float
    evidence: List[Dict[str, Any]]
    findings: List[str]
    tool_calls: List[str]
    graph_summary: Dict[str, Any]
    explanation: str
    next_action: str
    missing_evidence: List[str]
    uncertainty: str
    status: str
