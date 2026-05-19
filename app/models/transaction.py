"""Transaction model definition."""

from datetime import datetime
from decimal import Decimal

from bson import ObjectId
from pydantic import Field

from app.core.constants.enums import TransactionType
from app.models.base import BaseDocument, TimestampMixin


class TransactionModel(BaseDocument, TimestampMixin):
    """Transaction document model for MongoDB."""

    id: ObjectId | None = Field(default=None, alias="_id")
    user_id: ObjectId
    type: TransactionType
    amount: Decimal = Field(ge=0, decimal_places=2)
    category_id: ObjectId
    note: str | None = Field(default=None, max_length=500)
    transaction_date: datetime
    is_deleted: bool = Field(default=False)

    def to_dict(self) -> dict:
        """Convert model to dictionary for database operations."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        # Convert Decimal to float for MongoDB storage
        if "amount" in data:
            data["amount"] = float(data["amount"])
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "TransactionModel":
        """Create model instance from dictionary."""
        # Convert float back to Decimal
        if "amount" in data:
            data["amount"] = Decimal(str(data["amount"]))
        return cls(**data)
