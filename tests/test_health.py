import json
from django.test import Client

def test_health_endpoint_returns_ok():
    client = Client()
    resp = client.get("/health/")
    assert resp.status_code == 200
    data = json.loads(resp.content.decode())
    assert data.get("status") == "ok"
