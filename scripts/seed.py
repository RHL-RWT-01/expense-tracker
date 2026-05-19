"""Database seed script for development and testing."""

import asyncio
import random
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings
from app.core.constants.enums import TransactionType
from app.core.security import PasswordHandler


async def seed_database() -> None:
    """Seed the database with sample data."""
    settings = get_settings()

    print(f"Connecting to MongoDB at {settings.mongodb_url}...")
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_database]

    # Clear existing data
    print("Clearing existing data...")
    await db.users.delete_many({})
    await db.transactions.delete_many({})
    await db.categories.delete_many({"is_default": False})
    await db.refresh_tokens.delete_many({})

    # Create sample user
    print("Creating sample user...")
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "hashed_password": PasswordHandler.hash("Password123!"),
        "is_active": True,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "last_login": None,
        "password_changed_at": None,
    }
    result = await db.users.insert_one(user_data)
    user_id = result.inserted_id
    print(f"Created user: john@example.com (password: Password123!)")

    # Get categories
    categories = await db.categories.find({"is_default": True}).to_list(length=100)
    category_ids = [cat["_id"] for cat in categories]

    if not category_ids:
        print("No default categories found. Please run the application first.")
        return

    # Create sample transactions
    print("Creating sample transactions...")
    transactions = []

    # Generate transactions for the last 6 months
    now = datetime.now(UTC)

    for i in range(100):
        days_ago = random.randint(0, 180)
        transaction_date = now - timedelta(days=days_ago)

        tx_type = random.choice([TransactionType.INCOME, TransactionType.EXPENSE])

        if tx_type == TransactionType.INCOME:
            amount = random.choice([
                Decimal("3500.00"),  # Salary
                Decimal("500.00"),   # Freelance
                Decimal("100.00"),   # Other
                Decimal("1000.00"),  # Bonus
            ])
            notes = random.choice([
                "Monthly salary",
                "Freelance project",
                "Side income",
                "Bonus payment",
                "Dividend",
            ])
        else:
            amount = Decimal(str(random.randint(10, 500)))
            notes = random.choice([
                "Grocery shopping",
                "Restaurant dinner",
                "Uber ride",
                "Electric bill",
                "Internet bill",
                "Coffee",
                "Movie tickets",
                "Online shopping",
                "Gym membership",
                "Doctor visit",
                None,
            ])

        transactions.append({
            "user_id": user_id,
            "type": tx_type,
            "amount": float(amount),
            "category_id": random.choice(category_ids),
            "note": notes,
            "transaction_date": transaction_date,
            "is_deleted": False,
            "created_at": transaction_date,
            "updated_at": transaction_date,
        })

    await db.transactions.insert_many(transactions)
    print(f"Created {len(transactions)} sample transactions")

    # Create a custom category
    print("Creating custom category...")
    custom_category = {
        "name": "Investments",
        "user_id": user_id,
        "is_default": False,
        "created_at": datetime.now(UTC),
    }
    await db.categories.insert_one(custom_category)
    print("Created custom category: Investments")

    print("\nSeed completed successfully!")
    print("\nSample login credentials:")
    print("  Email: john@example.com")
    print("  Password: Password123!")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
