from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    evidence_id: str
    source: str
    summary: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidencePackage(BaseModel):
    case_id: str
    evidence: List[Evidence] = Field(default_factory=list)
