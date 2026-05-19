"""API routes module."""

from fastapi import APIRouter

from app.api.routes.analytics import router as analytics_router
from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as categories_router
from app.api.routes.health import router as health_router
from app.api.routes.transactions import router as transactions_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all route modules
api_router.include_router(auth_router)
api_router.include_router(transactions_router)
api_router.include_router(categories_router)
api_router.include_router(analytics_router)
api_router.include_router(health_router)

__all__ = ["api_router"]
