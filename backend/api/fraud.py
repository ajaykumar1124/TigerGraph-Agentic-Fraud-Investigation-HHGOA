from fastapi import APIRouter

from backend.data.ingestion import build_graph_context, load_real_dataset_bundle
from backend.models.events import FraudEvent
from backend.services.case_service import create_case

router = APIRouter()


@router.get("/fraud/investigation/{transaction_id}")
def get_transaction_investigation(transaction_id: str):
    try:
        bundle = load_real_dataset_bundle()
    except FileNotFoundError:
        return {
            "transaction_id": transaction_id,
            "transaction": {},
            "customer_id": None,
            "match_context": {},
            "history": [],
            "case_matches": [],
        }

    return build_graph_context(bundle, transaction_id)


@router.post("/fraud/events")
def receive_fraud_event(event: FraudEvent):
    case = create_case(
        transaction_id=event.transaction_id,
        event_type=event.event_type,
        risk_score=event.risk_score,
    )
    payload = case.model_dump()
    payload["risk"] = payload.get("risk", {})
    payload["recommended_actions"] = payload.get("recommended_actions", [])
    return payload
