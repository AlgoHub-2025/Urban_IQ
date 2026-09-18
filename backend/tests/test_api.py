import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_api_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "UrbanIQ Backend"
    assert "workflow_loaded" in data

def test_get_air_quality():
    response = client.get("/api/air-quality")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["live", "fallback"]
