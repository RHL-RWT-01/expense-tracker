"""Refresh token model definition."""

from datetime import UTC, datetime

from bson import ObjectId
from pydantic import Field

from app.models.base import BaseDocument


class RefreshTokenModel(BaseDocument):
    """Refresh token document model for MongoDB."""

    id: ObjectId | None = Field(default=None, alias="_id")
    user_id: ObjectId
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_revoked: bool = Field(default=False)
    device_info: str | None = Field(default=None)

    def to_dict(self) -> dict:
        """Convert model to dictionary for database operations."""
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict) -> "RefreshTokenModel":
        """Create model instance from dictionary."""
        return cls(**data)

    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now(UTC) > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not revoked and not expired)."""
        return not self.is_revoked and not self.is_expired
