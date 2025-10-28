import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "EduGrade AI Firebase backend running successfully"}

def test_verify_credential(client):
    response = client.post("/api/v1/devdock/verify", json={"credential": "test"})
    assert response.status_code == 200
    assert response.json() == {"verified": True}
