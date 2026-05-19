"""Analytics routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_analytics_service, get_current_active_user
from app.schemas.analytics import (
    AnalyticsParams,
    CategoryBreakdownResponse,
    MonthlyTrendsResponse,
    SummaryResponse,
)
from app.schemas.base import ResponseSchema
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/summary",
    response_model=ResponseSchema[SummaryResponse],
    summary="Get financial summary",
    description="Get total income, expense, and net balance for a period.",
)
async def get_summary(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    params: Annotated[AnalyticsParams, Query()],
) -> ResponseSchema[SummaryResponse]:
    """Get financial summary."""
    summary = await analytics_service.get_summary(
        user_id=current_user["id"],
        start_date=params.start_date,
        end_date=params.end_date,
    )

    return ResponseSchema(
        success=True,
        message="Summary retrieved successfully",
        data=summary,
    )


@router.get(
    "/category-breakdown",
    response_model=ResponseSchema[CategoryBreakdownResponse],
    summary="Get category breakdown",
    description="Get expense breakdown by category with percentages.",
)
async def get_category_breakdown(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    params: Annotated[AnalyticsParams, Query()],
) -> ResponseSchema[CategoryBreakdownResponse]:
    """Get category breakdown."""
    breakdown = await analytics_service.get_category_breakdown(
        user_id=current_user["id"],
        start_date=params.start_date,
        end_date=params.end_date,
    )

    return ResponseSchema(
        success=True,
        message="Category breakdown retrieved successfully",
        data=breakdown,
    )


@router.get(
    "/monthly-trends",
    response_model=ResponseSchema[MonthlyTrendsResponse],
    summary="Get monthly trends",
    description="Get income and expense trends over recent months.",
)
async def get_monthly_trends(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    params: Annotated[AnalyticsParams, Query()],
) -> ResponseSchema[MonthlyTrendsResponse]:
    """Get monthly trends."""
    trends = await analytics_service.get_monthly_trends(
        user_id=current_user["id"],
        months=params.months,
    )

    return ResponseSchema(
        success=True,
        message="Monthly trends retrieved successfully",
        data=trends,
    )
