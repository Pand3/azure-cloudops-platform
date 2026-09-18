"""Tests for Platform API request logging."""

import json
import logging
from io import StringIO
from uuid import UUID

from fastapi.testclient import TestClient
from platform_api.logging_config import JsonFormatter
from platform_api.main import app

client = TestClient(app)


def test_request_generates_request_id() -> None:
    """Requests without an ID should receive a generated UUID."""

    response = client.get("/health")

    assert response.status_code == 200

    request_id = response.headers["X-Request-ID"]

    assert str(UUID(request_id)) == request_id


def test_request_preserves_existing_request_id() -> None:
    """An ID supplied by the caller should be returned unchanged."""

    response = client.get(
        "/health",
        headers={"X-Request-ID": "test-request-123"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"


def test_request_writes_structured_json_log() -> None:
    """Completed requests should produce a structured JSON log entry."""

    log_output = StringIO()
    handler = logging.StreamHandler(log_output)
    handler.setFormatter(JsonFormatter())

    application_logger = logging.getLogger("platform_api")
    application_logger.addHandler(handler)

    try:
        response = client.get(
            "/health",
            headers={"X-Request-ID": "logging-test-123"},
        )
    finally:
        application_logger.removeHandler(handler)
        handler.close()

    log_lines = log_output.getvalue().strip().splitlines()
    log_data = json.loads(log_lines[-1])

    assert response.status_code == 200
    assert log_data["level"] == "INFO"
    assert log_data["event"] == "http_request"
    assert log_data["request_id"] == "logging-test-123"
    assert log_data["method"] == "GET"
    assert log_data["path"] == "/health"
    assert log_data["status_code"] == 200
    assert log_data["duration_ms"] >= 0
    assert "timestamp" in log_data
