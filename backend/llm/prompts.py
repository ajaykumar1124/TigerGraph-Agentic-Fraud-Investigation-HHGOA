"""System prompts and evidence formatting for the fraud-investigation agent."""

from __future__ import annotations

from typing import Any, Dict

FRAUD_INVESTIGATION_SYSTEM_PROMPT = """
You are a bank fraud investigation agent.

Your responsibility is to investigate suspicious transactions using graph evidence, behavioral patterns, and account context.

Rules:
1. Use the provided evidence, not assumptions.
2. Separate evidence from suspicion.
3. Identify the most relevant graph findings.
4. Explain why a transaction is suspicious.
5. State what evidence is still missing.
6. Recommend the next-best investigation step.
7. Never claim fraud based on a single weak signal.

Do not replace graph intelligence with free-form reasoning.
Your job is to reason over graph evidence and explain the investigation clearly.
"""


def build_investigation_prompt(transaction_id: str, evidence: Dict[str, Any]) -> str:
    """Build a structured fraud-investigation prompt for the LLM."""
    return f"""
Transaction ID: {transaction_id}

Evidence:
{evidence}

Please answer the following:
1. What does the evidence indicate?
2. What graph findings are most relevant?
3. What is the likely fraud pattern, if any?
4. What evidence is still missing?
5. Recommend the next-best action.

Use concise, evidence-based reasoning and avoid unsupported assumptions.
"""
