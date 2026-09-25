"""Wrapper around the LLM provider used for fraud investigation reasoning."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

try:
    from langchain_openai import ChatOpenAI
except Exception:  # pragma: no cover - optional dependency
    ChatOpenAI = None


def ask_llm(prompt: str, *, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
    """Ask the configured LLM for reasoning, or return a deterministic fallback if no API key exists."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    selected_model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")

    if not api_key or ChatOpenAI is None:
        return _fallback_reasoning(prompt)

    llm = ChatOpenAI(model=selected_model, api_key=api_key, temperature=0.0)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = llm.invoke(messages)
        return getattr(response, "content", str(response))
    except Exception:
        return _fallback_reasoning(prompt)


def _fallback_reasoning(prompt: str) -> str:
    """Use a deterministic rule-based fallback when an LLM provider is unavailable."""
    lower = prompt.lower()
    if "missing" in lower:
        return "The evidence is suggestive but incomplete. Additional device, customer, and network context is still required before a final determination."
    if "transaction" in lower and ("device" in lower or "network" in lower or "customer" in lower):
        return "The evidence indicates a pattern of elevated risk because device or customer context diverges from the expected profile. The investigation should continue with targeted graph checks and a review of customer verification." 
    return "The evidence supports a reasoned investigation path. The transaction should be reviewed with additional graph evidence before final policy action is assigned."
