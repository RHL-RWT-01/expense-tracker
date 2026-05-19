"""Base exception classes for the application."""

from typing import Any


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = 500,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)


class ValidationException(AppException):
    """Validation error exception."""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message=message, status_code=422, errors=errors)


class AuthenticationException(AppException):
    """Authentication error exception."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, status_code=401)


class AuthorizationException(AppException):
    """Authorization error exception."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message=message, status_code=403)


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message=message, status_code=404)


class ConflictException(AppException):
    """Resource conflict exception."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message=message, status_code=409)


class DatabaseException(AppException):
    """Database operation exception."""

    def __init__(self, message: str = "Database operation failed") -> None:
        super().__init__(message=message, status_code=500)


class RateLimitException(AppException):
    """Rate limit exceeded exception."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message=message, status_code=429)
