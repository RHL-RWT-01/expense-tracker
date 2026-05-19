"""Application lifespan management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database.mongodb import MongoDB
from app.core.logging import get_logger, setup_logging
from app.repositories.category import CategoryRepository

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown."""
    # Startup
    setup_logging()
    logger.info("Starting application...")

    # Connect to database
    mongodb = MongoDB()
    await mongodb.connect()

    # Initialize default categories
    category_repo = CategoryRepository(mongodb.database)
    await category_repo.initialize_defaults()

    logger.info("Application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await mongodb.disconnect()
    logger.info("Application shutdown complete")
