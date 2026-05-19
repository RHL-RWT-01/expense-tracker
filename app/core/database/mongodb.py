"""MongoDB connection and database management."""

from typing import Self

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class MongoDB:
    """MongoDB connection manager implementing singleton pattern."""

    _instance: Self | None = None
    _client: AsyncIOMotorClient | None = None
    _database: AsyncIOMotorDatabase | None = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """Establish connection to MongoDB."""
        if self._client is not None:
            return

        settings = get_settings()

        logger.info("Connecting to MongoDB", url=settings.mongodb_url)

        self._client = AsyncIOMotorClient(
            settings.mongodb_url,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000,
        )
        self._database = self._client[settings.mongodb_database]

        # Verify connection
        await self._client.admin.command("ping")
        logger.info("Successfully connected to MongoDB")

        # Initialize indexes
        await self._create_indexes()

    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self._client is not None:
            logger.info("Closing MongoDB connection")
            self._client.close()
            self._client = None
            self._database = None

    async def _create_indexes(self) -> None:
        """Create database indexes for optimal query performance."""
        if self._database is None:
            return

        logger.info("Creating database indexes")

        # Users collection indexes
        await self._database.users.create_index("email", unique=True)
        await self._database.users.create_index("created_at")

        # Transactions collection indexes
        await self._database.transactions.create_index("user_id")
        await self._database.transactions.create_index("category_id")
        await self._database.transactions.create_index("transaction_date")
        await self._database.transactions.create_index("created_at")
        await self._database.transactions.create_index([("user_id", 1), ("transaction_date", -1)])
        await self._database.transactions.create_index([("user_id", 1), ("type", 1)])

        # Categories collection indexes
        await self._database.categories.create_index("user_id")
        await self._database.categories.create_index("is_default")
        await self._database.categories.create_index([("user_id", 1), ("name", 1)], unique=True)

        # Refresh tokens collection indexes
        await self._database.refresh_tokens.create_index("user_id")
        await self._database.refresh_tokens.create_index("token", unique=True)
        await self._database.refresh_tokens.create_index("expires_at", expireAfterSeconds=0)

        logger.info("Database indexes created successfully")

    @property
    def client(self) -> AsyncIOMotorClient:
        """Get the MongoDB client instance."""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Get the database instance."""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database


# Global instance
_mongodb = MongoDB()


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database instance."""
    return _mongodb.database
