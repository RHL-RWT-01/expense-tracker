"""Transaction service for business logic."""

from datetime import datetime
from decimal import Decimal
from math import ceil
from typing import Any

from app.core.constants.enums import TransactionType
from app.core.exceptions import NotFoundException, ValidationException
from app.core.logging import get_logger
from app.repositories.category import CategoryRepository
from app.repositories.transaction import TransactionRepository
from app.schemas.base import PaginationMeta

logger = get_logger(__name__)


class TransactionService:
    """Service handling transaction-related business logic."""

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._transaction_repo = transaction_repository
        self._category_repo = category_repository

    async def create_transaction(
        self,
        user_id: str,
        type: TransactionType,
        amount: Decimal,
        category_id: str,
        transaction_date: datetime,
        note: str | None = None,
    ) -> dict[str, Any]:
        """Create a new transaction."""
        # Validate category exists and is accessible
        category = await self._category_repo.find_accessible_category(category_id, user_id)

        if not category:
            raise ValidationException("Category not found or not accessible")

        transaction = await self._transaction_repo.create(
            user_id=user_id,
            type=type,
            amount=amount,
            category_id=category_id,
            transaction_date=transaction_date,
            note=note,
        )

        # Add category name to response
        transaction["category_name"] = category["name"]

        logger.info(
            "Transaction created",
            transaction_id=transaction["id"],
            user_id=user_id,
            type=type,
        )

        return transaction

    async def get_transaction(
        self,
        transaction_id: str,
        user_id: str,
    ) -> dict[str, Any]:
        """Get a transaction by ID."""
        transaction = await self._transaction_repo.find_user_transaction(
            transaction_id,
            user_id,
        )

        if not transaction:
            raise NotFoundException("Transaction not found")

        # Get category name
        category = await self._category_repo.find_by_id(transaction["category_id"])
        if category:
            transaction["category_name"] = category["name"]

        return transaction

    async def list_transactions(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "transaction_date",
        sort_order: str = "desc",
        type: TransactionType | None = None,
        category_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        search: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ) -> tuple[list[dict[str, Any]], PaginationMeta]:
        """List transactions with filtering and pagination."""
        skip = (page - 1) * page_size

        # Get transactions
        transactions = await self._transaction_repo.find_by_user(
            user_id=user_id,
            skip=skip,
            limit=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
            type=type,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date,
            search=search,
            min_amount=min_amount,
            max_amount=max_amount,
        )

        # Get total count
        total = await self._transaction_repo.count_by_user(
            user_id=user_id,
            type=type,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date,
            search=search,
            min_amount=min_amount,
            max_amount=max_amount,
        )

        # Get category names
        category_ids = {t["category_id"] for t in transactions}
        categories = {}

        for cat_id in category_ids:
            cat = await self._category_repo.find_by_id(cat_id)
            if cat:
                categories[cat_id] = cat["name"]

        for transaction in transactions:
            transaction["category_name"] = categories.get(transaction["category_id"])

        # Calculate pagination metadata
        total_pages = ceil(total / page_size) if total > 0 else 0

        pagination = PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )

        return transactions, pagination

    async def update_transaction(
        self,
        transaction_id: str,
        user_id: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Update a transaction."""
        # Verify transaction exists and belongs to user
        existing = await self._transaction_repo.find_user_transaction(
            transaction_id,
            user_id,
        )

        if not existing:
            raise NotFoundException("Transaction not found")

        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return await self.get_transaction(transaction_id, user_id)

        # Validate category if being updated
        if "category_id" in update_data:
            category = await self._category_repo.find_accessible_category(
                update_data["category_id"],
                user_id,
            )
            if not category:
                raise ValidationException("Category not found or not accessible")

        transaction = await self._transaction_repo.update_transaction(
            transaction_id,
            user_id,
            update_data,
        )

        if not transaction:
            raise NotFoundException("Transaction not found")

        # Get category name
        category = await self._category_repo.find_by_id(transaction["category_id"])
        if category:
            transaction["category_name"] = category["name"]

        logger.info(
            "Transaction updated",
            transaction_id=transaction_id,
            user_id=user_id,
        )

        return transaction

    async def delete_transaction(
        self,
        transaction_id: str,
        user_id: str,
    ) -> None:
        """Soft delete a transaction."""
        success = await self._transaction_repo.soft_delete_transaction(
            transaction_id,
            user_id,
        )

        if not success:
            raise NotFoundException("Transaction not found")

        logger.info(
            "Transaction deleted",
            transaction_id=transaction_id,
            user_id=user_id,
        )
