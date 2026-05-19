"""Category model definition."""

from datetime import UTC, datetime

from bson import ObjectId
from pydantic import Field

from app.models.base import BaseDocument


class CategoryModel(BaseDocument):
    """Category document model for MongoDB."""

    id: ObjectId | None = Field(default=None, alias="_id")
    name: str = Field(min_length=1, max_length=50)
    user_id: ObjectId | None = Field(default=None)  # None for default categories
    is_default: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict:
        """Convert model to dictionary for database operations."""
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict) -> "CategoryModel":
        """Create model instance from dictionary."""
        return cls(**data)

    @property
    def is_user_owned(self) -> bool:
        """Check if category is owned by a user."""
        return self.user_id is not None and not self.is_default
