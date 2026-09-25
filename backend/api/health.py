from fastapi import APIRouter
from typing import Dict
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health_check() -> Dict:
    """Health check endpoint with TigerGraph status"""
    
    response = {
        "status": "healthy",
        "service": "TigerGraph Agentic Fraud Investigation",
        "version": "1.0.0"
    }
    
    # Try to check TigerGraph connection
    try:
        from backend.services.tigergraph_service import tigergraph_service
        tg_status = tigergraph_service.get_connection_status()
        response["tigergraph"] = tg_status
    except Exception as e:
        logger.warning(f"Could not check TigerGraph status: {e}")
        response["tigergraph"] = {
            "connected": False,
            "error": "Service not initialized"
        }
    
    return response

