"""Analyse structured CloudOps JSON log files."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LogSummary:
    """Summary calculated from a CloudOps log file."""

    total_lines: int
    valid_entries: int
    malformed_entries: int
    successful_checks: int
    failed_checks: int
    average_response_time_ms: float | None
    status_codes: dict[int, int]


class LogAnalysisError(Exception):
    """Raised when a log file cannot be analysed."""


def analyse_log(path: Path) -> LogSummary:
    """Read a JSON Lines log file and calculate operational statistics."""

    total_lines = 0
    valid_entries = 0
    malformed_entries = 0
    successful_checks = 0
    failed_checks = 0
    response_times: list[float] = []
    status_codes: dict[int, int] = {}

    try:
        with path.open(encoding="utf-8") as log_file:
            for line in log_file:
                if not line.strip():
                    continue

                total_lines += 1

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    malformed_entries += 1
                    continue

                if not isinstance(entry, dict):
                    malformed_entries += 1
                    continue

                valid_entries += 1

                event = entry.get("event")

                if event == "api_check_success":
                    successful_checks += 1
                elif event == "api_check_failure":
                    failed_checks += 1

                status_code = entry.get("status_code")

                if isinstance(status_code, int) and not isinstance(status_code, bool):
                    status_codes[status_code] = status_codes.get(status_code, 0) + 1

                response_time = entry.get("response_time_ms")

                if isinstance(response_time, int | float) and not isinstance(
                    response_time, bool
                ):
                    response_times.append(float(response_time))

    except OSError as error:
        raise LogAnalysisError(f"Could not read {path}: {error}") from error

    average_response_time = (
        sum(response_times) / len(response_times) if response_times else None
    )

    return LogSummary(
        total_lines=total_lines,
        valid_entries=valid_entries,
        malformed_entries=malformed_entries,
        successful_checks=successful_checks,
        failed_checks=failed_checks,
        average_response_time_ms=average_response_time,
        status_codes=status_codes,
    )
