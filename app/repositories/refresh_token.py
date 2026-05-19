"""Refresh token repository for database operations."""

from datetime import UTC, datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.utils.helpers import serialize_doc, to_objectid
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository):
    """Repository for refresh token-related database operations."""

    collection_name = "refresh_tokens"

    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        super().__init__(database)

    async def create(
        self,
        user_id: str,
        token: str,
        expires_at: datetime,
        device_info: str | None = None,
    ) -> dict[str, Any]:
        """Create a new refresh token."""
        document = {
            "user_id": to_objectid(user_id),
            "token": token,
            "expires_at": expires_at,
            "is_revoked": False,
            "device_info": device_info,
            "created_at": datetime.now(UTC),
        }

        token_id = await self.insert_one(document)
        return await self.find_by_id(token_id)

    async def find_valid_token(self, token: str) -> dict[str, Any] | None:
        """Find a valid (not revoked, not expired) refresh token."""
        doc = await self.collection.find_one(
            {
                "token": token,
                "is_revoked": False,
                "expires_at": {"$gt": datetime.now(UTC)},
            }
        )
        return serialize_doc(doc)

    async def find_by_token(self, token: str) -> dict[str, Any] | None:
        """Find a refresh token by its value."""
        doc = await self.collection.find_one({"token": token})
        return serialize_doc(doc)

    async def revoke_token(self, token: str) -> bool:
        """Revoke a specific refresh token."""
        result = await self.collection.update_one(
            {"token": token},
            {"$set": {"is_revoked": True}},
        )
        return result.modified_count > 0

    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user."""
        result = await self.collection.update_many(
            {
                "user_id": to_objectid(user_id),
                "is_revoked": False,
            },
            {"$set": {"is_revoked": True}},
        )
        return result.modified_count

    async def delete_expired_tokens(self) -> int:
        """Delete all expired tokens (cleanup task)."""
        result = await self.collection.delete_many(
            {
                "expires_at": {"$lt": datetime.now(UTC)},
            }
        )
        return result.deleted_count

    async def count_active_sessions(self, user_id: str) -> int:
        """Count active sessions for a user."""
        return await self.count(
            {
                "user_id": to_objectid(user_id),
                "is_revoked": False,
                "expires_at": {"$gt": datetime.now(UTC)},
            }
        )

    async def find_user_sessions(self, user_id: str) -> list[dict[str, Any]]:
        """Find all active sessions for a user."""
        return await self.find_many(
            {
                "user_id": to_objectid(user_id),
                "is_revoked": False,
                "expires_at": {"$gt": datetime.now(UTC)},
            },
            sort=[("created_at", -1)],
        )
