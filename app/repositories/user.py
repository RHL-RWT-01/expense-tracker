"""User repository for database operations."""

from datetime import UTC, datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.utils.helpers import serialize_doc
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for user-related database operations."""

    collection_name = "users"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database)

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        """Find a user by email address."""
        doc = await self.collection.find_one({"email": email.lower()})
        return serialize_doc(doc)

    async def find_by_id_with_password(self, user_id: str) -> dict[str, Any] | None:
        """Find a user by ID including the hashed password."""
        from app.core.utils.helpers import to_objectid

        doc = await self.collection.find_one({"_id": to_objectid(user_id)})
        if doc:
            doc["id"] = str(doc.pop("_id"))
        return doc

    async def create(
        self,
        name: str,
        email: str,
        hashed_password: str,
    ) -> dict[str, Any]:
        """Create a new user."""
        now = datetime.now(UTC)

        document = {
            "name": name,
            "email": email.lower(),
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "last_login": None,
            "password_changed_at": None,
        }

        user_id = await self.insert_one(document)
        return await self.find_by_id(user_id)

    async def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp."""
        return await self.update_one(user_id, {"last_login": datetime.now(UTC)})

    async def update_password(self, user_id: str, hashed_password: str) -> bool:
        """Update user's password."""
        return await self.update_one(
            user_id,
            {
                "hashed_password": hashed_password,
                "password_changed_at": datetime.now(UTC),
            },
        )

    async def email_exists(self, email: str, exclude_user_id: str | None = None) -> bool:
        """Check if an email already exists."""
        filter = {"email": email.lower()}
        if exclude_user_id:
            from app.core.utils.helpers import to_objectid

            filter["_id"] = {"$ne": to_objectid(exclude_user_id)}
        return await self.exists(filter)

    async def deactivate(self, user_id: str) -> bool:
        """Deactivate a user account."""
        return await self.update_one(user_id, {"is_active": False})

    async def activate(self, user_id: str) -> bool:
        """Activate a user account."""
        return await self.update_one(user_id, {"is_active": True})
