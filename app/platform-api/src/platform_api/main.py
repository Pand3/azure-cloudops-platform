"""FastAPI application deployed by the CloudOps platform."""

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from platform_api.config import get_settings
from platform_api.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CloudOps Platform API",
    description="Operational workload for the Azure CloudOps Platform",
    version="0.1.0",
)


@app.middleware("http")
async def log_http_request(request: Request, call_next) -> Response:
    """Record one structured log entry for every HTTP request."""

    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    start_time = perf_counter()

    response = await call_next(request)

    duration_ms = (perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "HTTP request completed",
        extra={
            "event": "http_request",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    return response


## Health and Operations Endpoints
@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Report whether the application process is running."""

    return {"status": "healthy"}


## Readiness Probe
@app.get("/ready", tags=["health"])
async def readiness() -> dict[str, str]:
    """Report whether the application can receive traffic."""

    get_settings()
    return {"status": "ready"}


### Liveness Probe
@app.get("/version", tags=["operations"])
async def version() -> dict[str, str]:
    """Report the running application version and environment."""

    settings = get_settings()

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
