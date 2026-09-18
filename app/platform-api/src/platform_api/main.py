"""FastAPI application deployed by the CloudOps platform."""

from fastapi import FastAPI

app = FastAPI(
    title="CloudOps Platform API",
    description="Operational workload for the Azure CloudOps Platform",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Report whether the application process is running."""

    return {"status": "healthy"}
