from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Trigger(BaseModel):
    type: str
    risk_score: float


class CaseRecord(BaseModel):
    case_id: str
    transaction_id: str
    status: str = "NEW"
    trigger: Trigger
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)
    uncertainty: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    timeline: List[str] = Field(default_factory=list)
    risk: Dict[str, Any] = Field(default_factory=dict)
    recommended_actions: List[str] = Field(default_factory=list)


class CaseCreateResult(BaseModel):
    case_id: str
    status: str
