"""User service for business logic."""

from typing import Any

from app.core.exceptions import NotFoundException
from app.core.logging import get_logger
from app.repositories.user import UserRepository

logger = get_logger(__name__)


class UserService:
    """Service handling user-related business logic."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repo = user_repository

    async def get_user(self, user_id: str) -> dict[str, Any]:
        """Get user by ID."""
        user = await self._user_repo.find_by_id(user_id)

        if not user:
            raise NotFoundException("User not found")

        return user

    async def update_user(
        self,
        user_id: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Update user profile."""
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return await self.get_user(user_id)

        success = await self._user_repo.update_one(user_id, update_data)

        if not success:
            raise NotFoundException("User not found")

        logger.info("User profile updated", user_id=user_id)

        return await self.get_user(user_id)

    async def deactivate_user(self, user_id: str) -> None:
        """Deactivate user account."""
        success = await self._user_repo.deactivate(user_id)

        if not success:
            raise NotFoundException("User not found")

        logger.info("User account deactivated", user_id=user_id)
