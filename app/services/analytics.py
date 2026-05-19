"""Analytics service for business logic."""

import calendar
from datetime import datetime
from decimal import Decimal

from app.core.logging import get_logger
from app.repositories.transaction import TransactionRepository
from app.schemas.analytics import (
    CategoryBreakdown,
    CategoryBreakdownResponse,
    MonthlyTrend,
    MonthlyTrendsResponse,
    SummaryResponse,
)

logger = get_logger(__name__)


class AnalyticsService:
    """Service handling analytics business logic."""

    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self._transaction_repo = transaction_repository

    async def get_summary(
        self,
        user_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> SummaryResponse:
        """Get financial summary for a user."""
        summary = await self._transaction_repo.get_summary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return SummaryResponse(
            total_income=summary["total_income"],
            total_expense=summary["total_expense"],
            net_balance=summary["net_balance"],
            transaction_count=summary["transaction_count"],
            period_start=start_date,
            period_end=end_date,
        )

    async def get_category_breakdown(
        self,
        user_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> CategoryBreakdownResponse:
        """Get expense breakdown by category."""
        breakdown = await self._transaction_repo.get_category_breakdown(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        # Calculate total for percentages
        total_expense = sum(Decimal(str(item["total_amount"])) for item in breakdown)

        categories = []
        for item in breakdown:
            amount = Decimal(str(item["total_amount"]))
            percentage = (
                (amount / total_expense * 100).quantize(Decimal("0.01"))
                if total_expense > 0
                else Decimal("0")
            )

            categories.append(
                CategoryBreakdown(
                    category_id=item["category_id"],
                    category_name=item["category_name"],
                    total_amount=amount,
                    transaction_count=item["transaction_count"],
                    percentage=percentage,
                )
            )

        return CategoryBreakdownResponse(
            total_expense=total_expense,
            categories=categories,
            period_start=start_date,
            period_end=end_date,
        )

    async def get_monthly_trends(
        self,
        user_id: str,
        months: int = 6,
    ) -> MonthlyTrendsResponse:
        """Get monthly income/expense trends."""
        trends_data = await self._transaction_repo.get_monthly_trends(
            user_id=user_id,
            months=months,
        )

        trends = []
        for item in trends_data:
            month_name = calendar.month_name[item["month"]]
            income = item["income"]
            expense = item["expense"]

            trends.append(
                MonthlyTrend(
                    year=item["year"],
                    month=item["month"],
                    month_name=month_name,
                    income=income,
                    expense=expense,
                    net=income - expense,
                    transaction_count=item["transaction_count"],
                )
            )

        return MonthlyTrendsResponse(
            trends=trends,
            total_months=len(trends),
        )
