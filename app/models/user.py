"""User model definition."""

from datetime import UTC, datetime

from bson import ObjectId
from pydantic import EmailStr, Field

from app.models.base import BaseDocument, TimestampMixin


class UserModel(BaseDocument, TimestampMixin):
    """User document model for MongoDB."""

    id: ObjectId | None = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = Field(default=True)
    last_login: datetime | None = Field(default=None)
    password_changed_at: datetime | None = Field(default=None)

    def to_dict(self, exclude_password: bool = True) -> dict:
        """Convert model to dictionary for database operations."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        if exclude_password and "hashed_password" in data:
            del data["hashed_password"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "UserModel":
        """Create model instance from dictionary."""
        return cls(**data)

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)

    def update_password_changed(self) -> None:
        """Update the password changed timestamp."""
        self.password_changed_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
