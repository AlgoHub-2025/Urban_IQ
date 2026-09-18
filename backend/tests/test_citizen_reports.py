from fastapi.testclient import TestClient
from api import app
import io
import os

client = TestClient(app)

def test_citizen_report_validations():
    # Helper to simulate file upload
    def make_request(filename="test.jpg", content_type="image/jpeg", content=b"fake image content", lat=31.52, lon=74.35):
        file_obj = io.BytesIO(content)
        return client.post(
            "/api/reports",
            files={"image": (filename, file_obj, content_type)},
            data={
                "latitude": str(lat),
                "longitude": str(lon),
                "zone_id": "gulberg",
                "category": "Waterlogging",
                "description": "Test"
            }
        )

    # 1. Invalid coordinates (outside region)
    res = make_request(lat=50.0, lon=10.0)
    assert res.status_code == 400
    assert "operational region (Lahore)" in res.json()["detail"]

    # 2. Invalid MIME type
    res = make_request(content_type="application/pdf", filename="test.pdf")
    assert res.status_code == 400
    assert "Invalid file type" in res.json()["detail"]

    # 3. Invalid extension
    res = make_request(filename="test.exe", content_type="image/jpeg")
    assert res.status_code == 400
    assert "Invalid file extension" in res.json()["detail"]

    # 4. Too large file
    large_content = b"0" * (6 * 1024 * 1024) # 6 MB
    res = make_request(content=large_content)
    assert res.status_code == 413
    assert "File too large" in res.json()["detail"]

    # 5. Success case
    res = make_request()
    assert res.status_code == 200
    assert res.json()["report"]["status"] == "pending"
    assert res.json()["report"]["ai_classification"] == "AI assessment unavailable \u2014 Human Review Required."
