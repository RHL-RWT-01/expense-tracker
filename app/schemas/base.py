"""Base schema definitions for API responses."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    has_next: bool
    has_previous: bool


class ResponseSchema(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = True
    message: str = "Success"
    data: T | None = None
    meta: dict[str, Any] | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response wrapper."""

    success: bool = True
    message: str = "Success"
    data: list[T] = Field(default_factory=list)
    meta: PaginationMeta


class ErrorDetail(BaseModel):
    """Error detail schema."""

    field: str | None = None
    message: str
    code: str | None = None


class ErrorResponse(BaseModel):
    """Error response schema."""

    success: bool = False
    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)
