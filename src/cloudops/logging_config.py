"""Structured logging configuration for CloudOps."""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

EXTRA_FIELDS = (
    "event",
    "url",
    "status_code",
    "response_time_ms",
    "config_path",
    "error",
)


class JsonFormatter(logging.Formatter):
    """Format log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        """Convert a Python log record into a JSON string."""

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

        return json.dumps(log_data)


def setup_logging(log_file: Path = Path("logs/cloudops.log")) -> None:
    """Configure the CloudOps logger to write structured JSON logs."""

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("cloudops")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    for existing_handler in logger.handlers:
        existing_handler.close()

    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())

    logger.addHandler(file_handler)
