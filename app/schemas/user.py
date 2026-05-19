"""User schemas."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema


class UserResponse(BaseSchema):
    """User response schema (public data only)."""

    id: str
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None


class UserUpdate(BaseModel):
    """User update request schema."""

    name: Annotated[str | None, Field(min_length=2, max_length=100)] = None

    @classmethod
    def has_updates(cls, data: "UserUpdate") -> bool:
        """Check if any fields are being updated."""
        return any(v is not None for v in data.model_dump().values())
