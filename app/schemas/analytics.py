"""Analytics schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class AnalyticsParams(BaseModel):
    """Analytics query parameters."""

    start_date: datetime | None = None
    end_date: datetime | None = None
    months: int = Field(default=6, ge=1, le=24)


class SummaryResponse(BaseSchema):
    """Financial summary response schema."""

    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal
    transaction_count: int
    period_start: datetime | None = None
    period_end: datetime | None = None


class CategoryBreakdown(BaseModel):
    """Category breakdown item schema."""

    category_id: str
    category_name: str
    total_amount: Decimal
    transaction_count: int
    percentage: Decimal


class CategoryBreakdownResponse(BaseSchema):
    """Category breakdown response schema."""

    total_expense: Decimal
    categories: list[CategoryBreakdown]
    period_start: datetime | None = None
    period_end: datetime | None = None


class MonthlyTrend(BaseModel):
    """Monthly trend item schema."""

    year: int
    month: int
    month_name: str
    income: Decimal
    expense: Decimal
    net: Decimal
    transaction_count: int


class MonthlyTrendsResponse(BaseSchema):
    """Monthly trends response schema."""

    trends: list[MonthlyTrend]
    total_months: int
