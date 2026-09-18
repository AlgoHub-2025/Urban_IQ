from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_auth_roles():
    # Test operator endpoint with viewer (should fail)
    response = client.post("/api/ai/query", headers={"X-Role": "viewer"}, json={"query": "test"})
    assert response.status_code == 403
    
    # Test operator endpoint with operator (should succeed or return 404/validation but not 403)
    response = client.post("/api/ai/query", headers={"X-Role": "operator"}, json={"query": "test"})
    assert response.status_code != 403
    
    # Test simulator endpoint with viewer
    response = client.post("/api/simulator/run", headers={"X-Role": "viewer"}, json={"zone_id": "gulberg"})
    assert response.status_code == 403
    
    # Test twin endpoint with viewer
    response = client.post("/api/twin/evaluate-action", headers={"X-Role": "viewer"}, json={"zone_id": "gulberg", "action": "test"})
    assert response.status_code == 403
