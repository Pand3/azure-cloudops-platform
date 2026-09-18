"""REST API health-checking functionality."""

from dataclasses import dataclass
from time import perf_counter
from typing import Any

import httpx


@dataclass(frozen=True)
class ApiCheckResult:
    """Successful API health-check result."""

    url: str
    status_code: int
    response_time_ms: float
    data: dict[str, Any]


class ApiCheckError(Exception):
    """Raised when an API health check fails."""


def check_api(
    base_url: str,
    timeout_seconds: float,
    health_path: str = "/get",
) -> ApiCheckResult:
    """Check an API endpoint and return its response information."""

    url = f"{base_url.rstrip('/')}/{health_path.lstrip('/')}"
    start_time = perf_counter()

    try:
        response = httpx.get(url, timeout=timeout_seconds)
    except httpx.TimeoutException as error:
        raise ApiCheckError(
            f"Request to {url} timed out after {timeout_seconds} seconds"
        ) from error
    except httpx.RequestError as error:
        raise ApiCheckError(f"Could not connect to {url}: {error}") from error

    response_time_ms = (perf_counter() - start_time) * 1000

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise ApiCheckError(
            f"API returned HTTP {response.status_code} for {url}"
        ) from error

    try:
        data = response.json()
    except ValueError as error:
        raise ApiCheckError(f"API returned invalid JSON from {url}") from error

    if not isinstance(data, dict):
        raise ApiCheckError(f"API returned JSON that was not an object from {url}")

    return ApiCheckResult(
        url=url,
        status_code=response.status_code,
        response_time_ms=response_time_ms,
        data=data,
    )
