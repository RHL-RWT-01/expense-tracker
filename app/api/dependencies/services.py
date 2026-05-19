"""Service dependencies for dependency injection."""

from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.repositories.category import CategoryRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.services.analytics import AnalyticsService
from app.services.auth import AuthService
from app.services.category import CategoryService
from app.services.transaction import TransactionService
from app.services.user import UserService


async def get_user_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> UserRepository:
    """Get user repository instance."""
    return UserRepository(database)


async def get_token_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> RefreshTokenRepository:
    """Get refresh token repository instance."""
    return RefreshTokenRepository(database)


async def get_transaction_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> TransactionRepository:
    """Get transaction repository instance."""
    return TransactionRepository(database)


async def get_category_repository(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> CategoryRepository:
    """Get category repository instance."""
    return CategoryRepository(database)


async def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    token_repo: Annotated[RefreshTokenRepository, Depends(get_token_repository)],
) -> AuthService:
    """Get auth service instance."""
    return AuthService(user_repo, token_repo)


async def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Get user service instance."""
    return UserService(user_repo)


async def get_transaction_service(
    transaction_repo: Annotated[TransactionRepository, Depends(get_transaction_repository)],
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> TransactionService:
    """Get transaction service instance."""
    return TransactionService(transaction_repo, category_repo)


async def get_category_service(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
) -> CategoryService:
    """Get category service instance."""
    return CategoryService(category_repo)


async def get_analytics_service(
    transaction_repo: Annotated[TransactionRepository, Depends(get_transaction_repository)],
) -> AnalyticsService:
    """Get analytics service instance."""
    return AnalyticsService(transaction_repo)
