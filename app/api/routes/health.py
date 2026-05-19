"""Health check routes."""

from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running and healthy.",
)
async def health_check() -> dict:
    """Basic health check endpoint."""
    settings = get_settings()

    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get(
    "/health/ready",
    summary="Readiness check",
    description="Check if the API is ready to accept requests.",
)
async def readiness_check() -> dict:
    """Readiness check including database connectivity."""
    from app.core.database.mongodb import _mongodb

    # Check database connection
    try:
        await _mongodb.client.admin.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ready" if db_status == "connected" else "not_ready",
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": {
            "database": db_status,
        },
    }
