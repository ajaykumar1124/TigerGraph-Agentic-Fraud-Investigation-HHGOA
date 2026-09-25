"""Investigation API endpoints - FastAPI integration for 6-phase LangGraph workflow."""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory case storage (in production, use database)
case_storage: Dict[str, Dict[str, Any]] = {}
agent: Optional[Any] = None
policy_engine: Optional[Any] = None
case_memory: Optional[Any] = None
USE_MOCK = True  # Start with mock, switch to real when dependencies are available


# Initialize with mock cases
def initialize_mock_cases():
    """Initialize some mock investigation cases for testing"""
    mock_cases = [
        {
            "case_id": "CASE-2026-001",
            "user_id": "USR_1001",
            "transaction_id": "TXN_2026_001",
            "initial_risk_level": "CRITICAL",
            "risk_indicators": ["velocity_check", "device_mismatch", "geographic_anomaly"],
            "confidence_score": 0.92,
            "recommended_action": "BLOCK",
            "reasoning": "Multiple high-value transactions from unusual locations with device mismatch detected",
            "case_status": "OPEN",
            "phase": 6,
            "status": "COMPLETED"
        },
        {
            "case_id": "CASE-2026-004",
            "user_id": "USR_1002",
            "transaction_id": "TXN_2026_002",
            "initial_risk_level": "CRITICAL",
            "risk_indicators": ["high_risk_country", "unusual_time", "large_amount"],
            "confidence_score": 0.94,
            "recommended_action": "BLOCK",
            "reasoning": "Large wire transfer to high-risk jurisdiction at unusual hour",
            "case_status": "OPEN",
            "phase": 6,
            "status": "COMPLETED"
        },
        {
            "case_id": "CASE-2026-007",
            "user_id": "USR_1003",
            "transaction_id": "TXN_2026_003",
            "initial_risk_level": "HIGH",
            "risk_indicators": ["crypto_related", "kyc_mismatch", "high_risk_country"],
            "confidence_score": 0.96,
            "recommended_action": "CHALLENGE",
            "reasoning": "Large cryptocurrency exchange transaction with KYC mismatches",
            "case_status": "IN_PROGRESS",
            "phase": 5,
            "status": "IN_PROGRESS"
        },
        {
            "case_id": "CASE-2026-003",
            "user_id": "USR_1001",
            "transaction_id": "TXN_2026_004",
            "initial_risk_level": "HIGH",
            "risk_indicators": ["unusual_time", "large_amount", "location_anomaly"],
            "confidence_score": 0.89,
            "recommended_action": "HOLD",
            "reasoning": "Large ATM withdrawal at unusual hour from Chennai",
            "case_status": "INVESTIGATING",
            "phase": 4,
            "status": "IN_PROGRESS"
        }
    ]
    
    for case in mock_cases:
        case_id = case["case_id"]
        case_storage[case_id] = {
            "state": case,
            "created_at": "2026-09-23T10:00:00",
            "started": True,
            "completed": case["status"] == "COMPLETED",
            "completed_at": "2026-09-23T17:00:00" if case["status"] == "COMPLETED" else None
        }
    
    logger.info(f"✅ Initialized {len(mock_cases)} mock investigation cases")

# Initialize mock data on module load
initialize_mock_cases()


def get_case_memory():
    """Get or initialize case memory."""
    global case_memory
    if case_memory is None:
        try:
            from backend.memory.case_storage import get_case_memory as get_memory
            case_memory = get_memory()
        except ImportError:
            logger.warning("Case memory module not available")
    return case_memory


def try_load_agent():
    """Try to load real agent, fall back to mock if dependencies missing."""
    global agent, policy_engine, USE_MOCK
    
    if agent is not None:
        return agent
    
    # Skip loading for now - use mock mode
    USE_MOCK = True
    logger.info("Using MOCK mode (real agent loading disabled)")
    return None


def get_mock_state(case_id: str, user_id: str, txn_id: str) -> Dict[str, Any]:
    """Generate mock investigation state for testing."""
    import random
    
    risk_level = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    
    return {
        "case_id": case_id,
        "user_id": user_id,
        "transaction_id": txn_id,
        "phase": 6,
        "status": "COMPLETED",
        "initial_risk_level": risk_level,
        "case_status": "OPEN",
        "risk_indicators": ["velocity_check", "device_mismatch", "merchant_risk"],
        "confidence_score": random.uniform(0.6, 0.95),
        "uncertainty_score": random.uniform(0.05, 0.4),
        "recommended_action": random.choice(["ALLOW", "HOLD", "CHALLENGE", "BLOCK"]),
        "action_confidence": random.uniform(0.7, 0.99),
        "reasoning": f"Mock analysis for case {case_id}: Multiple risk indicators detected during 6-phase investigation",
        "policy_violations": [] if risk_level in ["LOW", "MEDIUM"] else ["HIGH_VELOCITY_TXN"],
        "patterns_matched": ["unusual_amount", "time_anomaly"] if risk_level in ["HIGH", "CRITICAL"] else [],
        "case_notes": f"Case {case_id} processed in mock mode through all 6 phases"
    }


class StartInvestigationRequest(BaseModel):
    """Request to start a new investigation."""
    user_id: str
    transaction_id: str
    initiator: str = "system"
    risk_indicators: Optional[List[str]] = None
    initial_risk_level: str = "MEDIUM"


class CaseResponse(BaseModel):
    """Response model for investigation case."""
    case_id: str
    user_id: str
    transaction_id: str
    status: str
    phase: int
    risk_level: str
    confidence_score: float
    recommended_action: Optional[str] = None
    reasoning: Optional[str] = None


@router.post("/investigations/start")
async def start_investigation(request: StartInvestigationRequest) -> Dict[str, Any]:
    """
    Start a new fraud investigation.
    
    Creates a new case and initializes the 6-phase investigation workflow.
    """
    case_id = f"CASE_{uuid.uuid4().hex[:8].upper()}"
    
    try:
        # Create initial state
        if USE_MOCK:
            state = get_mock_state(case_id, request.user_id, request.transaction_id)
        else:
            from backend.agents.investigation_state import create_initial_state
            state = create_initial_state(
                case_id=case_id,
                user_id=request.user_id,
                transaction_id=request.transaction_id,
                initiator=request.initiator,
                risk_indicators=request.risk_indicators or [],
                initial_risk_level=request.initial_risk_level
            )
        
        # Store case
        case_storage[case_id] = {
            "state": state,
            "created_at": datetime.now().isoformat(),
            "started": False,
            "completed": False
        }
        
        logger.info(f"✓ Investigation started: {case_id}")
        
        return {
            "case_id": case_id,
            "status": "CREATED",
            "message": f"Investigation case {case_id} created for user {request.user_id}",
            "mode": "MOCK" if USE_MOCK else "PRODUCTION",
            "next_action": f"POST /api/v1/investigations/{case_id}/run"
        }
    except Exception as e:
        logger.error(f"✗ Error starting investigation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/investigations/{case_id}/run")
async def run_investigation(case_id: str) -> Dict[str, Any]:
    """
    Run the 6-phase investigation workflow.
    
    Executes all investigation phases and returns recommendation.
    """
    if case_id not in case_storage:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    
    case_data = case_storage[case_id]
    
    if case_data["completed"]:
        return {
            "case_id": case_id,
            "status": "ALREADY_COMPLETED",
            "message": "Investigation already completed"
        }
    
    try:
        logger.info(f"[{case_id}] Running investigation workflow...")
        
        # Get agent and run investigation
        agent = try_load_agent()
        state = case_data["state"]
        
        if USE_MOCK or agent is None:
            # Use mock result
            result_state = state.copy()
            result_state["phase"] = 6
            result_state["status"] = "COMPLETED"
        else:
            # Use real agent
            result = agent.invoke(
                case_id=state["case_id"],
                user_id=state["user_id"],
                transaction_id=state["transaction_id"]
            )
            result_state = result.get("state", state)
        
        # Store result
        case_data["state"] = result_state
        case_data["started"] = True
        case_data["completed"] = True
        case_data["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"✓ Investigation completed: {case_id}")
        
        # Extract key results
        return {
            "case_id": case_id,
            "status": "COMPLETED",
            "phase": result_state.get("phase", 6),
            "mode": "MOCK" if USE_MOCK else "PRODUCTION",
            "risk_indicators": result_state.get("risk_indicators", []),
            "initial_risk_level": result_state.get("initial_risk_level"),
            "recommended_action": result_state.get("recommended_action", "PENDING"),
            "action_confidence": result_state.get("action_confidence", 0.0),
            "reasoning": result_state.get("reasoning", ""),
            "policy_violations": result_state.get("policy_violations", []),
            "patterns_matched": result_state.get("patterns_matched", []),
            "case_status": result_state.get("case_status", "OPEN")
        }
    except Exception as e:
        logger.error(f"✗ Investigation failed for {case_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/investigations/{case_id}")
async def get_investigation(case_id: str) -> CaseResponse:
    """Get investigation details for a case."""
    if case_id not in case_storage:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    
    case_data = case_storage[case_id]
    state = case_data["state"]
    
    return CaseResponse(
        case_id=state.get("case_id"),
        user_id=state.get("user_id"),
        transaction_id=state.get("transaction_id"),
        status=state.get("case_status", "OPEN"),
        phase=state.get("phase", 0),
        risk_level=state.get("initial_risk_level", "MEDIUM"),
        confidence_score=state.get("confidence_score", 0.0),
        recommended_action=state.get("recommended_action"),
        reasoning=state.get("reasoning")
    )


@router.get("/investigations/{case_id}/details")
async def get_investigation_details(case_id: str) -> Dict[str, Any]:
    """Get full investigation details including evidence and patterns."""
    if case_id not in case_storage:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    
    case_data = case_storage[case_id]
    state = case_data["state"]
    
    # Mock policy evaluation
    risk_score = 0.75 if state.get("initial_risk_level") == "HIGH" else 0.5
    policy_eval = {
        "case_id": case_id,
        "action": state.get("recommended_action", "ALLOW"),
        "requires_approval": risk_score > 0.7,
        "approval_role": "ANALYST" if risk_score > 0.7 else None,
        "policy_rationale": f"Risk level {state.get('initial_risk_level')}"
    }
    
    return {
        "case_id": case_id,
        "created_at": case_data.get("created_at"),
        "completed_at": case_data.get("completed_at"),
        "status": state.get("case_status", "OPEN"),
        "phase": state.get("phase", 0),
        "user_id": state.get("user_id"),
        "transaction_id": state.get("transaction_id"),
        "risk_indicators": state.get("risk_indicators", []),
        "initial_risk_level": state.get("initial_risk_level"),
        "confidence_score": state.get("confidence_score", 0.0),
        "uncertainty_score": state.get("uncertainty_score", 1.0),
        "patterns_matched": state.get("patterns_matched", []),
        "policies_triggered": state.get("policies_triggered", []),
        "related_cases": state.get("related_cases", []),
        "recommended_action": state.get("recommended_action", "PENDING"),
        "action_confidence": state.get("action_confidence", 0.0),
        "reasoning": state.get("reasoning", ""),
        "policy_violations": state.get("policy_violations", []),
        "policy_evaluation": policy_eval,
        "case_notes": state.get("case_notes", ""),
        "mode": "MOCK" if USE_MOCK else "PRODUCTION"
    }


@router.get("/investigations")
async def list_investigations() -> Dict[str, Any]:
    """List all investigations."""
    cases = []
    for case_id, case_data in case_storage.items():
        state = case_data["state"]
        cases.append({
            "case_id": case_id,
            "user_id": state.get("user_id"),
            "transaction_id": state.get("transaction_id"),
            "status": state.get("case_status", "OPEN"),
            "phase": state.get("phase", 0),
            "risk_level": state.get("initial_risk_level"),
            "confidence_score": state.get("confidence_score", 0.0),
            "recommended_action": state.get("recommended_action", "PENDING"),
            "created_at": case_data.get("created_at"),
            "completed_at": case_data.get("completed_at")
        })
    
    return {
        "total": len(cases),
        "mode": "MOCK" if USE_MOCK else "PRODUCTION",
        "cases": cases
    }


@router.get("/investigations/{case_id}/recommendation")
async def get_recommendation(case_id: str) -> Dict[str, Any]:
    """Get the recommended action for a case."""
    if case_id not in case_storage:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    
    case_data = case_storage[case_id]
    state = case_data["state"]
    
    if not state.get("recommended_action"):
        return {"error": "No recommendation yet"}
    
    # Mock policy evaluation
    risk_score = 0.75 if state.get("initial_risk_level") == "HIGH" else 0.5
    policy_eval = {
        "case_id": case_id,
        "action": state.get("recommended_action"),
        "requires_approval": risk_score > 0.7,
        "approval_role": "ANALYST" if risk_score > 0.7 else None,
        "policy_rationale": f"Risk level {state.get('initial_risk_level')}"
    }
    
    return {
        "case_id": case_id,
        "recommended_action": state.get("recommended_action"),
        "action_confidence": state.get("action_confidence", 0.0),
        "reasoning": state.get("reasoning", ""),
        "policy_violations": state.get("policy_violations", []),
        "policy_evaluation": policy_eval,
        "requires_approval": policy_eval.get("requires_approval", False),
        "approval_role": policy_eval.get("approval_role"),
        "mode": "MOCK" if USE_MOCK else "PRODUCTION"
    }


class RecordOutcomeRequest(BaseModel):
    """Request to record investigation outcome."""
    actual_fraud: bool
    action_taken: str = "NONE"
    notes: str = ""


@router.post("/investigations/{case_id}/outcome")
async def record_outcome(case_id: str, request: RecordOutcomeRequest) -> Dict[str, Any]:
    """Record the actual outcome of an investigation."""
    if case_id not in case_storage:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    
    try:
        case_data = case_storage[case_id]
        state = case_data["state"]
        memory = get_case_memory()
        
        # Record outcome
        outcome = {
            "case_id": case_id,
            "predicted_fraud": state.get("recommended_action") in ["HOLD", "CHALLENGE", "BLOCK"],
            "actual_fraud": request.actual_fraud,
            "confidence": state.get("action_confidence", 0.0),
            "action_taken": request.action_taken,
            "notes": request.notes
        }
        
        # Save to memory
        if memory:
            memory.record_outcome(outcome)
            
            # Save case for later analysis
            memory.save_case({
                "case_id": case_id,
                "state": state,
                "outcome": outcome
            })
        
        # Update case storage
        case_data["outcome"] = outcome
        case_data["outcome_recorded_at"] = datetime.now().isoformat()
        
        logger.info(f"✓ Outcome recorded for {case_id}: actual={request.actual_fraud}, predicted={outcome['predicted_fraud']}")
        
        return {
            "case_id": case_id,
            "status": "OUTCOME_RECORDED",
            "outcome": outcome
        }
    except Exception as e:
        logger.error(f"✗ Error recording outcome: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/investigations/analytics/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get analytics metrics from case memory."""
    try:
        memory = get_case_memory()
        if not memory:
            return {"error": "Case memory not available"}
        
        stats = memory.get_statistics()
        patterns = memory.learn_patterns()
        
        return {
            "status": "ok",
            "statistics": stats,
            "patterns_learned": patterns
        }
    except Exception as e:
        logger.error(f"✗ Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
