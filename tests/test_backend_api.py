from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "bankguard"}


def test_fraud_event_creates_case():
    response = client.post(
        "/api/v1/fraud/events",
        json={
            "event_type": "RISK_SIGNAL",
            "transaction_id": "TX123",
            "risk_score": 0.91,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "NEW"
    assert payload["case_id"].startswith("CASE-")


def test_case_lookup_returns_created_case():
    create_response = client.post(
        "/api/v1/fraud/events",
        json={
            "event_type": "RISK_SIGNAL",
            "transaction_id": "TX456",
            "risk_score": 0.81,
        },
    )
    case_id = create_response.json()["case_id"]

    get_response = client.get(f"/api/v1/cases/{case_id}")
    assert get_response.status_code == 200
    payload = get_response.json()
    assert payload["case_id"] == case_id
    assert payload["transaction_id"] == "TX456"
    assert payload["status"] == "NEW"


def test_graph_investigation_endpoint_uses_real_dataset_context():
    response = client.get("/api/v1/fraud/investigation/TX00000001")
    assert response.status_code == 200
    payload = response.json()
    assert payload["transaction"]["TransactionID"] == "TX00000001"
    assert payload["transaction"]["customer_id"] == "C000103"
    assert "history" in payload
    assert payload["match_context"] or payload["history"]


def test_fraud_event_case_includes_graph_evidence_when_dataset_is_available():
    response = client.post(
        "/api/v1/fraud/events",
        json={
            "event_type": "RISK_SIGNAL",
            "transaction_id": "TX00000001",
            "risk_score": 0.95,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["case_id"].startswith("CASE-")
    assert "evidence" in payload
    assert payload["evidence"]


def test_fraud_event_uses_deterministic_risk_pipeline():
    response = client.post(
        "/api/v1/fraud/events",
        json={
            "event_type": "RISK_SIGNAL",
            "transaction_id": "TX00000001",
            "risk_score": 0.95,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "risk" in payload
    assert payload["risk"]["source"] == "rules_ml_graph"
    assert 0.0 <= payload["risk"]["score"] <= 1.0
    assert payload["recommended_actions"]
