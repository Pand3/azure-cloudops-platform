"""Tests for the CloudOps Platform API."""

from fastapi.testclient import TestClient
from platform_api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """The health endpoint should report a healthy application."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
