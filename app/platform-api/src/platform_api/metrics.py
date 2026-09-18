"""Prometheus metrics for the Platform API."""

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "platform_api_http_requests_total",
    "Total HTTP requests processed by the Platform API.",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "platform_api_http_request_duration_seconds",
    "Time spent processing Platform API requests.",
    ["method", "path"],
)


def record_request(
    *,
    method: str,
    path: str,
    status_code: int,
    duration_seconds: float,
) -> None:
    """Record the result and duration of one HTTP request."""

    HTTP_REQUESTS.labels(
        method=method,
        path=path,
        status_code=str(status_code),
    ).inc()

    HTTP_REQUEST_DURATION.labels(
        method=method,
        path=path,
    ).observe(duration_seconds)


def render_metrics() -> tuple[bytes, str]:
    """Return metrics in the Prometheus exposition format."""

    return generate_latest(), CONTENT_TYPE_LATEST
