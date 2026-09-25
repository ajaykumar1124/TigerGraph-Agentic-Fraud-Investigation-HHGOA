from pydantic import BaseModel, Field


class FraudEvent(BaseModel):
    event_type: str = Field(..., description="Type of fraud signal")
    transaction_id: str = Field(..., description="Transaction identifier")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0 and 1")

    class Config:
        extra = "forbid"
