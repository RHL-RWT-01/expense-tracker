"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthenticationException
from app.core.security import JWTHandler
from app.repositories.user import UserRepository

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    """Get the current authenticated user from JWT token."""
    token = credentials.credentials

    # Verify token
    payload = JWTHandler.verify_access_token(token)

    # Get database and user
    from app.core.database.mongodb import _mongodb

    database = _mongodb.database
    user_repo = UserRepository(database)

    user = await user_repo.find_by_id(payload.sub)

    if not user:
        raise AuthenticationException("User not found")

    return user


async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """Get the current active user."""
    if not current_user.get("is_active", True):
        raise AuthenticationException("Account is deactivated")

    return current_user
