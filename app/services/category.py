"""Category service for business logic."""

from typing import Any

from app.core.exceptions import (
    AuthorizationException,
    ConflictException,
    NotFoundException,
    ValidationException,
)
from app.core.logging import get_logger
from app.repositories.category import CategoryRepository

logger = get_logger(__name__)


class CategoryService:
    """Service handling category-related business logic."""

    def __init__(self, category_repository: CategoryRepository) -> None:
        self._category_repo = category_repository

    async def initialize_defaults(self) -> None:
        """Initialize default categories."""
        await self._category_repo.initialize_defaults()
        logger.info("Default categories initialized")

    async def list_categories(self, user_id: str) -> list[dict[str, Any]]:
        """List all categories available to a user."""
        return await self._category_repo.find_all_for_user(user_id)

    async def create_category(
        self,
        user_id: str,
        name: str,
    ) -> dict[str, Any]:
        """Create a new custom category."""
        # Check if name already exists
        if await self._category_repo.name_exists_for_user(name, user_id):
            raise ConflictException(f"Category '{name}' already exists")

        category = await self._category_repo.create(
            name=name,
            user_id=user_id,
        )

        logger.info(
            "Category created",
            category_id=category["id"],
            user_id=user_id,
        )

        return category

    async def get_category(
        self,
        category_id: str,
        user_id: str,
    ) -> dict[str, Any]:
        """Get a category by ID."""
        category = await self._category_repo.find_accessible_category(category_id, user_id)

        if not category:
            raise NotFoundException("Category not found")

        return category

    async def update_category(
        self,
        category_id: str,
        user_id: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Update a category."""
        # Verify category exists and is owned by user
        existing = await self._category_repo.find_by_id(category_id)

        if not existing:
            raise NotFoundException("Category not found")

        if existing.get("is_default"):
            raise AuthorizationException("Cannot modify default categories")

        if existing.get("user_id") != user_id:
            raise AuthorizationException("Cannot modify categories you don't own")

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return existing

        # Check for name conflicts
        if "name" in update_data:
            if await self._category_repo.name_exists_for_user(
                update_data["name"],
                user_id,
                exclude_id=category_id,
            ):
                raise ConflictException(f"Category '{update_data['name']}' already exists")

        category = await self._category_repo.update_category(
            category_id,
            user_id,
            update_data,
        )

        if not category:
            raise NotFoundException("Category not found")

        logger.info(
            "Category updated",
            category_id=category_id,
            user_id=user_id,
        )

        return category

    async def delete_category(
        self,
        category_id: str,
        user_id: str,
    ) -> None:
        """Delete a category."""
        # Verify category exists
        existing = await self._category_repo.find_by_id(category_id)

        if not existing:
            raise NotFoundException("Category not found")

        if existing.get("is_default"):
            raise AuthorizationException("Cannot delete default categories")

        if existing.get("user_id") != user_id:
            raise AuthorizationException("Cannot delete categories you don't own")

        # Check if category is in use
        if await self._category_repo.is_category_in_use(category_id):
            raise ValidationException("Cannot delete category that is used in transactions")

        success = await self._category_repo.delete_category(category_id, user_id)

        if not success:
            raise NotFoundException("Category not found")

        logger.info(
            "Category deleted",
            category_id=category_id,
            user_id=user_id,
        )
