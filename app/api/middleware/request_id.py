"""Request ID middleware for request tracing."""

import uuid
from collections.abc import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware for adding unique request IDs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add request ID to request and response."""
        # Get existing request ID from header or generate new one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store in request state
        request.state.request_id = request_id

        # Bind to structlog context
        structlog.contextvars.bind_contextvars(request_id=request_id)

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Clear context
        structlog.contextvars.clear_contextvars()

        return response
