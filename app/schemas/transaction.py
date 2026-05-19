"""Transaction schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from app.core.constants.enums import TransactionType
from app.schemas.base import BaseSchema


class TransactionCreate(BaseModel):
    """Transaction creation request schema."""

    type: TransactionType
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    category_id: str
    note: Annotated[str | None, Field(max_length=500)] = None
    transaction_date: datetime

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate amount precision."""
        return round(v, 2)


class TransactionUpdate(BaseModel):
    """Transaction update request schema."""

    type: TransactionType | None = None
    amount: Annotated[Decimal | None, Field(gt=0, decimal_places=2)] = None
    category_id: str | None = None
    note: Annotated[str | None, Field(max_length=500)] = None
    transaction_date: datetime | None = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal | None) -> Decimal | None:
        """Validate amount precision."""
        if v is not None:
            return round(v, 2)
        return v


class TransactionResponse(BaseSchema):
    """Transaction response schema."""

    id: str
    user_id: str
    type: TransactionType
    amount: Decimal
    category_id: str
    category_name: str | None = None
    note: str | None = None
    transaction_date: datetime
    created_at: datetime
    updated_at: datetime


class TransactionListParams(BaseModel):
    """Transaction list query parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="transaction_date")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    type: TransactionType | None = None
    category_id: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    search: str | None = Field(default=None, max_length=100)
    min_amount: Decimal | None = Field(default=None, ge=0)
    max_amount: Decimal | None = Field(default=None, ge=0)
