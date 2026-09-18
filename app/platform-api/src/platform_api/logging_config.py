"""Structured logging for the Platform API."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

EXTRA_FIELDS = (
    "event",
    "request_id",
    "method",
    "path",
    "status_code",
    "duration_ms",
)


class JsonFormatter(logging.Formatter):
    """Format application logs as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        """Convert a log record into JSON."""

        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=UTC,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in EXTRA_FIELDS:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure structured logging to standard output."""

    logger = logging.getLogger("platform_api")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    for existing_handler in logger.handlers:
        existing_handler.close()

    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
