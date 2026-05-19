"""Pydantic schemas module."""

from app.schemas.analytics import (
    AnalyticsParams,
    CategoryBreakdown,
    CategoryBreakdownResponse,
    MonthlyTrend,
    MonthlyTrendsResponse,
    SummaryResponse,
)
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.base import PaginatedResponse, PaginationMeta, ResponseSchema
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.transaction import (
    TransactionCreate,
    TransactionListParams,
    TransactionResponse,
    TransactionUpdate,
)
from app.schemas.user import UserResponse, UserUpdate

__all__ = [
    # Base
    "ResponseSchema",
    "PaginatedResponse",
    "PaginationMeta",
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    # User
    "UserResponse",
    "UserUpdate",
    # Transaction
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
    "TransactionListParams",
    # Category
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    # Analytics
    "SummaryResponse",
    "CategoryBreakdown",
    "CategoryBreakdownResponse",
    "MonthlyTrend",
    "MonthlyTrendsResponse",
    "AnalyticsParams",
]
