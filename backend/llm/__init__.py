"""LLM integration layer for fraud investigation reasoning."""

from .model import ask_llm
from .prompts import FRAUD_INVESTIGATION_SYSTEM_PROMPT, build_investigation_prompt

__all__ = ["ask_llm", "FRAUD_INVESTIGATION_SYSTEM_PROMPT", "build_investigation_prompt"]
