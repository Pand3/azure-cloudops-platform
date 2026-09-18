"""Tests for the CloudOps Platform API."""

from fastapi.testclient import TestClient
from platform_api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """The health endpoint should report a healthy application."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_endpoint() -> None:
    """The readiness endpoint should report that traffic can be accepted."""

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_version_endpoint() -> None:
    """The version endpoint should expose safe build information."""

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "cloudops-platform-api",
        "version": "0.1.0",
        "environment": "dev",
    }


def test_version_endpoint_uses_environment_variables(monkeypatch) -> None:
    """Version information should be configurable without changing code."""

    monkeypatch.setenv("PLATFORM_APP_NAME", "deployed-platform-api")
    monkeypatch.setenv("PLATFORM_APP_VERSION", "abc1234")
    monkeypatch.setenv("PLATFORM_ENVIRONMENT", "staging")

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "deployed-platform-api",
        "version": "abc1234",
        "environment": "staging",
    }
