"""Tests for structured CloudOps logging."""

import json
import logging

from cloudops.logging_config import setup_logging


def test_setup_logging_writes_structured_json(tmp_path) -> None:
    """Logging should create directories and write valid JSON."""

    log_file = tmp_path / "nested" / "cloudops.log"
    setup_logging(log_file)

    logger = logging.getLogger("cloudops.test")
    logger.info(
        "Test event completed",
        extra={
            "event": "test_success",
            "status_code": 200,
        },
    )

    log_content = log_file.read_text(encoding="utf-8")
    log_data = json.loads(log_content)

    assert log_file.exists()
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "cloudops.test"
    assert log_data["message"] == "Test event completed"
    assert log_data["event"] == "test_success"
    assert log_data["status_code"] == 200
    assert "timestamp" in log_data
