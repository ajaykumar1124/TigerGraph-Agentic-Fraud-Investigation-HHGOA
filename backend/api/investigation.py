"""
Investigation API Endpoints
AI-powered fraud investigation using LLM
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from backend.services.llm_investigation_agent import fraud_investigation_agent
from backend.services.tigergraph_service import tigergraph_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/investigation", tags=["Investigation"])


class InvestigationRequest(BaseModel):
    """Investigation request model"""
    case_id: str
    include_user_data: bool = True
    max_transactions: int = 10


class TransactionInvestigationRequest(BaseModel):
    """Single transaction investigation"""
    transaction_id: str


class CaseAnalysisResponse(BaseModel):
    """Case analysis response"""
    case_id: str
    status: str
    analysis: Dict
    report: Optional[str] = None


@router.post("/analyze-case", response_model=CaseAnalysisResponse)
async def analyze_case(request: InvestigationRequest):
    """
    Analyze a fraud case using AI
    
    Provides intelligent insights including:
    - Pattern matching
    - Risk assessment
    - Investigation recommendations
    - Evidence summary
    """
    try:
        logger.info(f"🔍 Analyzing case: {request.case_id}")
        
        # Get case data from TigerGraph
        case = tigergraph_service.get_fraud_case_by_id(request.case_id)
        
        if not case:
            # Return "not found" training data
            return CaseAnalysisResponse(
                case_id=request.case_id,
                status="not_found",
                analysis={
                    "message": "Investigation not found",
                    "description": "This investigation could not be retrieved.",
                    "risk_score": 0.0,
                    "recommendations": [
                        "Verify case ID is correct",
                        "Check if case has been deleted",
                        "Contact system administrator"
                    ],
                    "timestamp": None
                },
                report=fraud_investigation_agent.generate_investigation_report(
                    {
                        "case_id": request.case_id,
                        "title": "Case Not Found",
                        "status": "not_found",
                        "severity": "unknown",
                        "description": "This investigation could not be retrieved.",
                        "created_at": None,
                        "assigned_to": None,
                        "amount_at_risk": 0
                    },
                    {
                        "risk_score": 0.0,
                        "analysis": "Investigation not found. This investigation could not be retrieved. Please verify the case ID and try again.",
                        "recommendations": ["Verify case ID", "Contact administrator"],
                        "pattern_matches": [],
                        "confidence": 0.0,
                        "model_used": "system"
                    }
                )
            )
        
        # Get related transactions
        transactions = tigergraph_service.get_case_transactions(
            request.case_id,
            limit=request.max_transactions
        )
        
        # Get user data if requested
        user_data = None
        if request.include_user_data and transactions:
            user_id = transactions[0].get('user_id')
            if user_id:
                user_data = tigergraph_service.get_user_by_id(user_id)
        
        # Run AI analysis
        analysis = fraud_investigation_agent.analyze_case(
            case_data=case,
            transactions=transactions,
            user_data=user_data
        )
        
        # Generate formal report
        report = fraud_investigation_agent.generate_investigation_report(
            case_data=case,
            analysis=analysis
        )
        
        logger.info(f"✅ Analysis complete: {request.case_id}")
        
        return CaseAnalysisResponse(
            case_id=request.case_id,
            status="completed",
            analysis=analysis,
            report=report
        )
        
    except Exception as e:
        logger.error(f"❌ Case analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/investigate-transaction")
async def investigate_transaction(request: TransactionInvestigationRequest):
    """
    Investigate a single transaction using AI
    
    Provides:
    - Fraud likelihood score
    - Red flags identified
    - Recommended action
    """
    try:
        logger.info(f"🔍 Investigating transaction: {request.transaction_id}")
        
        # Get transaction data
        transaction = tigergraph_service.get_transaction_by_id(request.transaction_id)
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Run AI investigation
        result = fraud_investigation_agent.investigate_transaction(transaction)
        
        logger.info(f"✅ Transaction investigation complete: {request.transaction_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Transaction investigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns")
async def get_fraud_patterns():
    """Get known fraud patterns used for training"""
    return {
        "patterns": fraud_investigation_agent.fraud_patterns,
        "protocols": fraud_investigation_agent.investigation_protocols
    }


@router.get("/health")
async def investigation_health():
    """Check investigation agent health"""
    
    is_ready = fraud_investigation_agent.client is not None
    
    return {
        "status": "ready" if is_ready else "limited",
        "llm_available": is_ready,
        "model": fraud_investigation_agent.model if is_ready else None,
        "fallback_mode": not is_ready,
        "message": "AI investigation ready" if is_ready else "Running in fallback mode (OpenAI API key required)"
    }
