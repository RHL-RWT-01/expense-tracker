"""Transaction repository for database operations."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.constants.enums import TransactionType
from app.core.utils.helpers import serialize_doc, to_objectid
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    """Repository for transaction-related database operations."""

    collection_name = "transactions"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database)

    async def create(
        self,
        user_id: str,
        type: TransactionType,
        amount: Decimal,
        category_id: str,
        transaction_date: datetime,
        note: str | None = None,
    ) -> dict[str, Any]:
        """Create a new transaction."""
        now = datetime.now(UTC)

        document = {
            "user_id": to_objectid(user_id),
            "type": type,
            "amount": float(amount),
            "category_id": to_objectid(category_id),
            "note": note,
            "transaction_date": transaction_date,
            "is_deleted": False,
            "created_at": now,
            "updated_at": now,
        }

        transaction_id = await self.insert_one(document)
        return await self.find_by_id(transaction_id)

    async def find_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "transaction_date",
        sort_order: str = "desc",
        type: TransactionType | None = None,
        category_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        search: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ) -> list[dict[str, Any]]:
        """Find transactions for a user with filtering and pagination."""
        filter = {
            "user_id": to_objectid(user_id),
            "is_deleted": False,
        }

        if type:
            filter["type"] = type

        if category_id:
            filter["category_id"] = to_objectid(category_id)

        if start_date:
            filter.setdefault("transaction_date", {})["$gte"] = start_date

        if end_date:
            filter.setdefault("transaction_date", {})["$lte"] = end_date

        if search:
            filter["note"] = {"$regex": search, "$options": "i"}

        if min_amount is not None:
            filter.setdefault("amount", {})["$gte"] = float(min_amount)

        if max_amount is not None:
            filter.setdefault("amount", {})["$lte"] = float(max_amount)

        sort_direction = -1 if sort_order == "desc" else 1
        sort = [(sort_by, sort_direction)]

        return await self.find_many(filter, skip=skip, limit=limit, sort=sort)

    async def count_by_user(
        self,
        user_id: str,
        type: TransactionType | None = None,
        category_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        search: str | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ) -> int:
        """Count transactions for a user with filtering."""
        filter = {
            "user_id": to_objectid(user_id),
            "is_deleted": False,
        }

        if type:
            filter["type"] = type

        if category_id:
            filter["category_id"] = to_objectid(category_id)

        if start_date:
            filter.setdefault("transaction_date", {})["$gte"] = start_date

        if end_date:
            filter.setdefault("transaction_date", {})["$lte"] = end_date

        if search:
            filter["note"] = {"$regex": search, "$options": "i"}

        if min_amount is not None:
            filter.setdefault("amount", {})["$gte"] = float(min_amount)

        if max_amount is not None:
            filter.setdefault("amount", {})["$lte"] = float(max_amount)

        return await self.count(filter)

    async def find_user_transaction(
        self,
        transaction_id: str,
        user_id: str,
    ) -> dict[str, Any] | None:
        """Find a transaction owned by a specific user."""
        doc = await self.collection.find_one(
            {
                "_id": to_objectid(transaction_id),
                "user_id": to_objectid(user_id),
                "is_deleted": False,
            }
        )
        return serialize_doc(doc)

    async def update_transaction(
        self,
        transaction_id: str,
        user_id: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Update a transaction owned by a specific user."""
        # Convert category_id if present
        if "category_id" in update_data:
            update_data["category_id"] = to_objectid(update_data["category_id"])

        # Convert amount to float if present
        if "amount" in update_data:
            update_data["amount"] = float(update_data["amount"])

        update_data["updated_at"] = datetime.now(UTC)

        result = await self.collection.update_one(
            {
                "_id": to_objectid(transaction_id),
                "user_id": to_objectid(user_id),
                "is_deleted": False,
            },
            {"$set": update_data},
        )

        if result.modified_count > 0:
            return await self.find_user_transaction(transaction_id, user_id)
        return None

    async def soft_delete_transaction(
        self,
        transaction_id: str,
        user_id: str,
    ) -> bool:
        """Soft delete a transaction owned by a specific user."""
        result = await self.collection.update_one(
            {
                "_id": to_objectid(transaction_id),
                "user_id": to_objectid(user_id),
                "is_deleted": False,
            },
            {
                "$set": {
                    "is_deleted": True,
                    "updated_at": datetime.now(UTC),
                }
            },
        )
        return result.modified_count > 0

    async def get_summary(
        self,
        user_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict[str, Any]:
        """Get financial summary for a user."""
        match_stage: dict[str, Any] = {
            "user_id": to_objectid(user_id),
            "is_deleted": False,
        }

        if start_date or end_date:
            match_stage["transaction_date"] = {}
            if start_date:
                match_stage["transaction_date"]["$gte"] = start_date
            if end_date:
                match_stage["transaction_date"]["$lte"] = end_date

        pipeline = [
            {"$match": match_stage},
            {
                "$group": {
                    "_id": "$type",
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1},
                }
            },
        ]

        results = await self.aggregate(pipeline)

        summary = {
            "total_income": Decimal("0"),
            "total_expense": Decimal("0"),
            "transaction_count": 0,
        }

        for item in results:
            if item["_id"] == TransactionType.INCOME:
                summary["total_income"] = Decimal(str(item["total"]))
            elif item["_id"] == TransactionType.EXPENSE:
                summary["total_expense"] = Decimal(str(item["total"]))
            summary["transaction_count"] += item["count"]

        summary["net_balance"] = summary["total_income"] - summary["total_expense"]

        return summary

    async def get_category_breakdown(
        self,
        user_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Get expense breakdown by category."""
        match_stage: dict[str, Any] = {
            "user_id": to_objectid(user_id),
            "type": TransactionType.EXPENSE,
            "is_deleted": False,
        }

        if start_date or end_date:
            match_stage["transaction_date"] = {}
            if start_date:
                match_stage["transaction_date"]["$gte"] = start_date
            if end_date:
                match_stage["transaction_date"]["$lte"] = end_date

        pipeline = [
            {"$match": match_stage},
            {
                "$group": {
                    "_id": "$category_id",
                    "total_amount": {"$sum": "$amount"},
                    "transaction_count": {"$sum": 1},
                }
            },
            {
                "$lookup": {
                    "from": "categories",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "category",
                }
            },
            {"$unwind": "$category"},
            {
                "$project": {
                    "category_id": {"$toString": "$_id"},
                    "category_name": "$category.name",
                    "total_amount": 1,
                    "transaction_count": 1,
                }
            },
            {"$sort": {"total_amount": -1}},
        ]

        return await self.aggregate(pipeline)

    async def get_monthly_trends(
        self,
        user_id: str,
        months: int = 6,
    ) -> list[dict[str, Any]]:
        """Get monthly income/expense trends."""
        pipeline = [
            {
                "$match": {
                    "user_id": to_objectid(user_id),
                    "is_deleted": False,
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$transaction_date"},
                        "month": {"$month": "$transaction_date"},
                        "type": "$type",
                    },
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id.year": -1, "_id.month": -1}},
        ]

        results = await self.aggregate(pipeline)

        # Process results into monthly trends
        months_data: dict[tuple[int, int], dict[str, Any]] = {}

        for item in results:
            key = (item["_id"]["year"], item["_id"]["month"])
            if key not in months_data:
                months_data[key] = {
                    "year": item["_id"]["year"],
                    "month": item["_id"]["month"],
                    "income": Decimal("0"),
                    "expense": Decimal("0"),
                    "transaction_count": 0,
                }

            if item["_id"]["type"] == TransactionType.INCOME:
                months_data[key]["income"] = Decimal(str(item["total"]))
            else:
                months_data[key]["expense"] = Decimal(str(item["total"]))

            months_data[key]["transaction_count"] += item["count"]

        # Sort and limit
        sorted_months = sorted(months_data.keys(), reverse=True)[:months]

        return [months_data[key] for key in sorted_months]
