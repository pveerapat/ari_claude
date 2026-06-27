from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_health_status():
    response = client.get("/health")
    assert response.status_code == 200


def test_root_health_body():
    response = client.get("/health")
    assert response.json() == {"status": "ok", "service": "ari-backend", "api": "/api/v1"}


def test_api_v1_health_status():
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_api_v1_health_body():
    response = client.get("/api/v1/health")
    assert response.json() == {"status": "ok", "service": "ari-backend", "api": "/api/v1"}


def test_request_id_header_returned():
    response = client.get("/health")
    assert "x-request-id" in response.headers


def test_request_id_echo():
    response = client.get("/health", headers={"X-Request-ID": "test-req-123"})
    assert response.headers.get("x-request-id") == "test-req-123"
