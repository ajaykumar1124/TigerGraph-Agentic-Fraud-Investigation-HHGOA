"""
Investigation State - LangGraph state management for fraud cases
Tracks all data through investigation workflow
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime


class InvestigationState(TypedDict):
    """Complete investigation state for LangGraph workflow"""
    
    # Initial case context
    case_id: str
    user_id: str
    transaction_id: str
    initiator: str
    risk_indicators: List[str]
    initial_risk_level: str
    
    # User context
    user_profile: Optional[Dict[str, Any]]
    user_risk_score: float
    
    # Transaction context
    transaction_details: Optional[Dict[str, Any]]
    merchant_profile: Optional[Dict[str, Any]]
    
    # Device & IP context
    device_details: Optional[Dict[str, Any]]
    ip_risk: Optional[Dict[str, Any]]
    
    # Evidence collection (Phase 2)
    retrieved_evidence: Optional[Dict[str, Any]]
    policies_triggered: List[Dict[str, Any]]
    patterns_matched: List[Dict[str, Any]]
    related_cases: List[Dict[str, Any]]
    evidence_summary: str
    
    # Uncertainty assessment (Phase 3)
    confidence_score: float
    uncertainty_score: float
    needs_additional_evidence: bool
    uncertainty_reason: str
    
    # Additional evidence (Phase 4, optional)
    additional_evidence_requested: bool
    evidence_request: str
    customer_response: str
    updated_evidence: Optional[Dict[str, Any]]
    
    # Recommendation (Phase 5)
    recommended_action: str
    action_confidence: float
    reasoning: str
    policy_violations: List[str]
    
    # Recording (Phase 6)
    case_status: str
    case_notes: str
    investigation_complete: bool
    
    # System metadata
    phase: int
    iteration_count: int
    max_iterations: int
    errors: List[str]
    workflow_start_time: str
    workflow_end_time: Optional[str]
    execution_time_ms: float


def create_initial_state(
    case_id: str,
    user_id: str,
    transaction_id: str,
    initiator: str = "system",
    risk_indicators: List[str] = None,
    initial_risk_level: str = "MEDIUM",
) -> InvestigationState:
    """Create initial investigation state"""
    
    return InvestigationState(
        # Initial context
        case_id=case_id,
        user_id=user_id,
        transaction_id=transaction_id,
        initiator=initiator,
        risk_indicators=risk_indicators or [],
        initial_risk_level=initial_risk_level,
        
        # User context
        user_profile=None,
        user_risk_score=0.0,
        
        # Transaction context
        transaction_details=None,
        merchant_profile=None,
        
        # Device & IP context
        device_details=None,
        ip_risk=None,
        
        # Evidence collection
        retrieved_evidence=None,
        policies_triggered=[],
        patterns_matched=[],
        related_cases=[],
        evidence_summary="",
        
        # Uncertainty assessment
        confidence_score=0.0,
        uncertainty_score=1.0,
        needs_additional_evidence=False,
        uncertainty_reason="",
        
        # Additional evidence
        additional_evidence_requested=False,
        evidence_request="",
        customer_response="",
        updated_evidence=None,
        
        # Recommendation
        recommended_action="PENDING",
        action_confidence=0.0,
        reasoning="",
        policy_violations=[],
        
        # Recording
        case_status="OPEN",
        case_notes="",
        investigation_complete=False,
        
        # System metadata
        phase=0,
        iteration_count=0,
        max_iterations=6,
        errors=[],
        workflow_start_time=datetime.now().isoformat(),
        workflow_end_time=None,
        execution_time_ms=0.0,
    )
