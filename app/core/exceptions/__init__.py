"""Custom exceptions module."""

from app.core.exceptions.base import (
    AppException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    DatabaseException,
    NotFoundException,
    RateLimitException,
    ValidationException,
)

__all__ = [
    "AppException",
    "AuthenticationException",
    "AuthorizationException",
    "ConflictException",
    "DatabaseException",
    "NotFoundException",
    "RateLimitException",
    "ValidationException",
]
