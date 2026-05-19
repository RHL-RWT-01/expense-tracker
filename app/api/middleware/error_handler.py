"""Centralized error handling middleware."""

from collections.abc import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppException
from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions globally."""

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """Process request and handle any exceptions."""
        try:
            return await call_next(request)
        except AppException as e:
            logger.warning(
                "Application error",
                error=e.message,
                status_code=e.status_code,
                errors=e.errors,
            )
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "message": e.message,
                    "errors": e.errors,
                },
            )
        except ValidationError as e:
            logger.warning("Validation error", errors=e.errors())
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "message": "Validation failed",
                    "errors": [
                        {
                            "field": ".".join(str(loc) for loc in err["loc"]),
                            "message": err["msg"],
                        }
                        for err in e.errors()
                    ],
                },
            )
        except Exception as e:
            logger.exception("Unexpected error", error=str(e))
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "An unexpected error occurred",
                    "errors": [],
                },
            )
