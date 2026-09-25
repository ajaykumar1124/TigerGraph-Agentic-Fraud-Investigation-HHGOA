from __future__ import annotations

from typing import Any, Dict, List


def compute_deterministic_risk(
    base_risk_score: float,
    evidence: List[Dict[str, Any]] | None = None,
    transaction_id: str | None = None,
) -> Dict[str, Any]:
    evidence = evidence or []
    score = float(base_risk_score)
    reasons: List[str] = [
        "Base model risk score applied as the first signal.",
    ]

    signal_count = 0
    has_device_match = False
    has_case_history = False
    has_case_pack_match = False

    for item in evidence:
        source = str(item.get("source", "")).lower()
        if "identity" in source:
            has_device_match = True
            signal_count += 1
            reasons.append("Identity/device evidence increased risk.")
        if "history" in source:
            has_case_history = True
            signal_count += 1
            reasons.append("Prior closed-case history increased risk.")
        if "case_pack" in source:
            has_case_pack_match = True
            signal_count += 1
            reasons.append("Case-pack pattern match increased risk.")
        if "transactions" in source:
            signal_count += 1

    score += min(signal_count * 0.08, 0.26)
    if has_device_match:
        score += 0.08
    if has_case_history:
        score += 0.10
    if has_case_pack_match:
        score += 0.12

    score = max(0.0, min(1.0, round(score, 4)))

    if transaction_id and str(transaction_id).startswith("TX"):
        score += 0.02
        reasons.append("Manual event routing was treated as a higher-priority trigger.")

    score = max(0.0, min(1.0, round(score, 4)))

    if score >= 0.85:
        actions = [
            "Freeze affected card and block additional spend.",
            "Request expedited customer confirmation and transaction review.",
            "Escalate to senior analyst with case summary and graph evidence.",
        ]
        policy_status = "escalate"
    elif score >= 0.65:
        actions = [
            "Review linked customer and device activity.",
            "Hold for fraud analyst validation before further action.",
            "Request recent transaction history from the customer.",
        ]
        policy_status = "review"
    else:
        actions = [
            "Continue monitoring for pattern changes.",
            "Collect additional transaction context and device linkage data.",
            "Document the event as low-confidence risk until more evidence arrives.",
        ]
        policy_status = "monitor"

    return {
        "source": "rules_ml_graph",
        "score": score,
        "confidence": round(min(0.92, 0.55 + score * 0.4), 4),
        "reasons": reasons,
        "policy_status": policy_status,
        "recommended_actions": actions,
    }
