from typing import Any, Dict

from backend.data.ingestion import build_graph_context, load_real_dataset_bundle
from backend.models.cases import CaseRecord
from backend.services.risk_engine import compute_deterministic_risk

_CASES: Dict[str, CaseRecord] = {}


def generate_case_id() -> str:
    next_id = len(_CASES) + 1
    return f"CASE-{next_id:06d}"


def _dataset_evidence(transaction_id: str) -> list[dict[str, Any]]:
    try:
        bundle = load_real_dataset_bundle()
    except FileNotFoundError:
        return []

    context = build_graph_context(bundle, transaction_id)
    evidence: list[dict[str, Any]] = []

    if context.get("transaction"):
        evidence.append(
            {
                "source": "transactions.csv",
                "entity": "Transaction",
                "details": {
                    "transaction_id": context["transaction"].get("TransactionID"),
                    "customer_id": context["transaction"].get("customer_id"),
                    "risk_score": context["transaction"].get("risk_score"),
                    "card_id": context["transaction"].get("card_id"),
                },
            }
        )

    if context.get("match_context"):
        evidence.append(
            {
                "source": "identity.csv",
                "entity": "DeviceIdentity",
                "details": context["match_context"],
            }
        )

    if context.get("history"):
        evidence.append(
            {
                "source": "closed_cases_history.csv",
                "entity": "CaseHistory",
                "details": {"recent_cases": context["history"]},
            }
        )

    if context.get("case_matches"):
        evidence.append(
            {
                "source": "case_pack.csv",
                "entity": "CasePack",
                "details": {"matches": context["case_matches"]},
            }
        )

    return evidence


def create_case(transaction_id: str, event_type: str, risk_score: float) -> CaseRecord:
    case_id = generate_case_id()
    evidence = _dataset_evidence(transaction_id)
    risk = compute_deterministic_risk(risk_score, evidence, transaction_id=transaction_id)
    findings = [
        f"Deterministic risk pipeline scored the event at {risk['score']:.3f} using rules + ML + graph evidence.",
    ]
    if evidence:
        findings.append(f"Transaction {transaction_id} matched dataset-backed investigation context.")

    case = CaseRecord(
        case_id=case_id,
        transaction_id=transaction_id,
        status="NEW",
        trigger={"type": event_type, "risk_score": risk_score},
        evidence=evidence,
        findings=findings,
        uncertainty=[] if evidence else ["No real dataset context was available for this event."],
        actions=[{"type": "risk_policy", "recommendation": action} for action in risk["recommended_actions"]],
        timeline=[
            f"{event_type} received for {transaction_id}",
            f"Deterministic risk engine output: {risk['score']:.3f} ({risk['policy_status']})",
        ],
        risk=risk,
        recommended_actions=risk["recommended_actions"],
    )
    _CASES[case_id] = case
    return case


def list_cases() -> Dict[str, CaseRecord]:
    return _CASES


def get_case(case_id: str) -> CaseRecord:
    if case_id not in _CASES:
        raise KeyError(case_id)
    return _CASES[case_id]
