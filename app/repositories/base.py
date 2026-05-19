"""Base repository with common database operations."""

from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.core.utils.helpers import serialize_doc, to_objectid

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository providing common CRUD operations."""

    collection_name: str

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database
        self._collection: AsyncIOMotorCollection = database[self.collection_name]

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Get the MongoDB collection."""
        return self._collection

    async def find_by_id(self, id: str) -> dict[str, Any] | None:
        """Find a document by its ID."""
        doc = await self.collection.find_one({"_id": to_objectid(id)})
        return serialize_doc(doc)

    async def find_one(self, filter: dict[str, Any]) -> dict[str, Any] | None:
        """Find a single document matching the filter."""
        doc = await self.collection.find_one(filter)
        return serialize_doc(doc)

    async def find_many(
        self,
        filter: dict[str, Any],
        skip: int = 0,
        limit: int = 20,
        sort: list[tuple[str, int]] | None = None,
    ) -> list[dict[str, Any]]:
        """Find multiple documents matching the filter."""
        cursor = self.collection.find(filter)

        if sort:
            cursor = cursor.sort(sort)

        cursor = cursor.skip(skip).limit(limit)

        docs = await cursor.to_list(length=limit)
        return [serialize_doc(doc) for doc in docs]

    async def count(self, filter: dict[str, Any]) -> int:
        """Count documents matching the filter."""
        return await self.collection.count_documents(filter)

    async def insert_one(self, document: dict[str, Any]) -> str:
        """Insert a single document and return its ID."""
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)

    async def update_one(
        self,
        id: str,
        update: dict[str, Any],
        upsert: bool = False,
    ) -> bool:
        """Update a single document by ID."""
        update_data = {
            "$set": {
                **update,
                "updated_at": datetime.now(UTC),
            }
        }

        result = await self.collection.update_one(
            {"_id": to_objectid(id)},
            update_data,
            upsert=upsert,
        )
        return result.modified_count > 0 or result.upserted_id is not None

    async def update_many(
        self,
        filter: dict[str, Any],
        update: dict[str, Any],
    ) -> int:
        """Update multiple documents matching the filter."""
        update_data = {
            "$set": {
                **update,
                "updated_at": datetime.now(UTC),
            }
        }

        result = await self.collection.update_many(filter, update_data)
        return result.modified_count

    async def delete_one(self, id: str) -> bool:
        """Delete a single document by ID (hard delete)."""
        result = await self.collection.delete_one({"_id": to_objectid(id)})
        return result.deleted_count > 0

    async def soft_delete(self, id: str) -> bool:
        """Soft delete a document by setting is_deleted flag."""
        return await self.update_one(id, {"is_deleted": True})

    async def delete_many(self, filter: dict[str, Any]) -> int:
        """Delete multiple documents matching the filter."""
        result = await self.collection.delete_many(filter)
        return result.deleted_count

    async def exists(self, filter: dict[str, Any]) -> bool:
        """Check if a document exists matching the filter."""
        count = await self.collection.count_documents(filter, limit=1)
        return count > 0

    async def aggregate(self, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Execute an aggregation pipeline."""
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=None)
