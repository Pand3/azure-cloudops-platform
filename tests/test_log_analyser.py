"""Tests for structured log analysis."""

from pathlib import Path

import pytest

from cloudops.log_analyser import LogAnalysisError, analyse_log


def test_analyse_mixed_log_entries(tmp_path: Path) -> None:
    """Valid, failed and malformed entries should be counted correctly."""

    log_file = tmp_path / "cloudops.log"
    log_file.write_text(
        """{"event":"api_check_success","status_code":200,"response_time_ms":100.0}
{"event":"api_check_success","status_code":200,"response_time_ms":300.0}
{"event":"api_check_failure","error":"Request timed out"}
this is not JSON
["valid JSON", "but not an object"]

""",
        encoding="utf-8",
    )

    summary = analyse_log(log_file)

    assert summary.total_lines == 5
    assert summary.valid_entries == 3
    assert summary.malformed_entries == 2
    assert summary.successful_checks == 2
    assert summary.failed_checks == 1
    assert summary.average_response_time_ms == 200.0
    assert summary.status_codes == {200: 2}


def test_analyse_empty_log(tmp_path: Path) -> None:
    """An empty log should return a summary containing zero values."""

    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    summary = analyse_log(log_file)

    assert summary.total_lines == 0
    assert summary.valid_entries == 0
    assert summary.malformed_entries == 0
    assert summary.successful_checks == 0
    assert summary.failed_checks == 0
    assert summary.average_response_time_ms is None
    assert summary.status_codes == {}


def test_reject_missing_log_file(tmp_path: Path) -> None:
    """A missing log file should produce a readable error."""

    missing_file = tmp_path / "missing.log"

    with pytest.raises(LogAnalysisError, match="Could not read"):
        analyse_log(missing_file)
