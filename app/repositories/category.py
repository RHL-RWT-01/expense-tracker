"""Category repository for database operations."""

from datetime import UTC, datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.constants.defaults import DEFAULT_CATEGORIES
from app.core.utils.helpers import serialize_doc, to_objectid
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    """Repository for category-related database operations."""

    collection_name = "categories"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database)

    async def initialize_defaults(self) -> None:
        """Initialize default categories if they don't exist."""
        for category_name in DEFAULT_CATEGORIES:
            exists = await self.exists(
                {
                    "name": category_name,
                    "is_default": True,
                }
            )

            if not exists:
                await self.collection.insert_one(
                    {
                        "name": category_name,
                        "user_id": None,
                        "is_default": True,
                        "created_at": datetime.now(UTC),
                    }
                )

    async def find_all_for_user(self, user_id: str) -> list[dict[str, Any]]:
        """Find all categories available to a user (defaults + user's custom)."""
        filter = {
            "$or": [
                {"is_default": True},
                {"user_id": to_objectid(user_id)},
            ]
        }
        return await self.find_many(filter, limit=1000, sort=[("name", 1)])

    async def find_defaults(self) -> list[dict[str, Any]]:
        """Find all default categories."""
        return await self.find_many({"is_default": True}, limit=100, sort=[("name", 1)])

    async def find_user_categories(self, user_id: str) -> list[dict[str, Any]]:
        """Find categories created by a specific user."""
        return await self.find_many(
            {"user_id": to_objectid(user_id)},
            limit=100,
            sort=[("name", 1)],
        )

    async def create(
        self,
        name: str,
        user_id: str,
    ) -> dict[str, Any]:
        """Create a new custom category for a user."""
        document = {
            "name": name,
            "user_id": to_objectid(user_id),
            "is_default": False,
            "created_at": datetime.now(UTC),
        }

        category_id = await self.insert_one(document)
        return await self.find_by_id(category_id)

    async def find_user_category(
        self,
        category_id: str,
        user_id: str,
    ) -> dict[str, Any] | None:
        """Find a category owned by a specific user."""
        doc = await self.collection.find_one(
            {
                "_id": to_objectid(category_id),
                "user_id": to_objectid(user_id),
                "is_default": False,
            }
        )
        return serialize_doc(doc)

    async def find_accessible_category(
        self,
        category_id: str,
        user_id: str,
    ) -> dict[str, Any] | None:
        """Find a category accessible to a user (default or owned)."""
        doc = await self.collection.find_one(
            {
                "_id": to_objectid(category_id),
                "$or": [
                    {"is_default": True},
                    {"user_id": to_objectid(user_id)},
                ],
            }
        )
        return serialize_doc(doc)

    async def update_category(
        self,
        category_id: str,
        user_id: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Update a category owned by a specific user."""
        result = await self.collection.update_one(
            {
                "_id": to_objectid(category_id),
                "user_id": to_objectid(user_id),
                "is_default": False,
            },
            {"$set": update_data},
        )

        if result.modified_count > 0:
            return await self.find_by_id(category_id)
        return None

    async def delete_category(
        self,
        category_id: str,
        user_id: str,
    ) -> bool:
        """Delete a category owned by a specific user."""
        result = await self.collection.delete_one(
            {
                "_id": to_objectid(category_id),
                "user_id": to_objectid(user_id),
                "is_default": False,
            }
        )
        return result.deleted_count > 0

    async def name_exists_for_user(
        self,
        name: str,
        user_id: str,
        exclude_id: str | None = None,
    ) -> bool:
        """Check if a category name already exists for a user."""
        filter: dict[str, Any] = {
            "name": {"$regex": f"^{name}$", "$options": "i"},
            "$or": [
                {"is_default": True},
                {"user_id": to_objectid(user_id)},
            ],
        }

        if exclude_id:
            filter["_id"] = {"$ne": to_objectid(exclude_id)}

        return await self.exists(filter)

    async def is_category_in_use(self, category_id: str) -> bool:
        """Check if a category is being used in any transaction."""
        transactions_collection = self.database["transactions"]
        count = await transactions_collection.count_documents(
            {"category_id": to_objectid(category_id), "is_deleted": False},
            limit=1,
        )
        return count > 0
