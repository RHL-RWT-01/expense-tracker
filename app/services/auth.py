"""Authentication service for business logic."""

from datetime import UTC, datetime, timedelta
from typing import Any

from app.core.config import get_settings
from app.core.exceptions import AuthenticationException, ConflictException
from app.core.logging import get_logger
from app.core.security import JWTHandler, PasswordHandler
from app.core.utils.helpers import generate_uuid
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository

logger = get_logger(__name__)


class AuthService:
    """Service handling authentication business logic."""

    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: RefreshTokenRepository,
    ) -> None:
        self._user_repo = user_repository
        self._token_repo = token_repository
        self._settings = get_settings()

    async def register(
        self,
        name: str,
        email: str,
        password: str,
    ) -> dict[str, Any]:
        """Register a new user."""
        # Check if email already exists
        if await self._user_repo.email_exists(email):
            raise ConflictException("Email already registered")

        # Hash password
        hashed_password = PasswordHandler.hash(password)

        # Create user
        user = await self._user_repo.create(
            name=name,
            email=email,
            hashed_password=hashed_password,
        )

        logger.info("User registered successfully", user_id=user["id"], email=email)

        return user

    async def login(
        self,
        email: str,
        password: str,
        device_info: str | None = None,
    ) -> dict[str, Any]:
        """Authenticate user and return tokens."""
        # Find user by email (including password for verification)
        user = await self._user_repo.find_by_email(email)

        if not user:
            # Use constant time comparison to prevent timing attacks
            PasswordHandler.verify("dummy", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.aaaaaaaaaaaaaaa")
            raise AuthenticationException("Invalid email or password")

        # Get user with password
        user_with_password = await self._user_repo.find_by_id_with_password(user["id"])

        if not user_with_password:
            raise AuthenticationException("Invalid email or password")

        # Verify password
        if not PasswordHandler.verify(password, user_with_password["hashed_password"]):
            raise AuthenticationException("Invalid email or password")

        # Check if user is active
        if not user_with_password.get("is_active", True):
            raise AuthenticationException("Account is deactivated")

        # Generate tokens
        tokens = await self._create_tokens(user["id"], device_info)

        # Update last login
        await self._user_repo.update_last_login(user["id"])

        logger.info("User logged in", user_id=user["id"])

        return {
            "user": user,
            "tokens": tokens,
        }

    async def refresh_tokens(self, refresh_token: str) -> dict[str, Any]:
        """Refresh access and refresh tokens."""
        # Verify refresh token
        try:
            payload = JWTHandler.verify_refresh_token(refresh_token)
        except AuthenticationException:
            raise AuthenticationException("Invalid refresh token")

        # Check if token exists and is valid in database
        stored_token = await self._token_repo.find_valid_token(refresh_token)

        if not stored_token:
            raise AuthenticationException("Refresh token is invalid or expired")

        # Revoke old token (token rotation)
        await self._token_repo.revoke_token(refresh_token)

        # Get user
        user = await self._user_repo.find_by_id(payload.sub)

        if not user:
            raise AuthenticationException("User not found")

        if not user.get("is_active", True):
            raise AuthenticationException("Account is deactivated")

        # Generate new tokens
        tokens = await self._create_tokens(user["id"])

        logger.info("Tokens refreshed", user_id=user["id"])

        return tokens

    async def logout(self, refresh_token: str) -> None:
        """Logout user by revoking refresh token."""
        await self._token_repo.revoke_token(refresh_token)
        logger.info("User logged out")

    async def logout_all(self, user_id: str) -> int:
        """Logout user from all sessions."""
        count = await self._token_repo.revoke_all_user_tokens(user_id)
        logger.info("User logged out from all sessions", user_id=user_id, sessions=count)
        return count

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> None:
        """Change user's password."""
        # Get user with current password
        user = await self._user_repo.find_by_id_with_password(user_id)

        if not user:
            raise AuthenticationException("User not found")

        # Verify current password
        if not PasswordHandler.verify(current_password, user["hashed_password"]):
            raise AuthenticationException("Current password is incorrect")

        # Hash new password
        new_hashed_password = PasswordHandler.hash(new_password)

        # Update password
        await self._user_repo.update_password(user_id, new_hashed_password)

        # Revoke all refresh tokens for security
        await self._token_repo.revoke_all_user_tokens(user_id)

        logger.info("Password changed", user_id=user_id)

    async def _create_tokens(
        self,
        user_id: str,
        device_info: str | None = None,
    ) -> dict[str, Any]:
        """Create access and refresh tokens."""
        # Generate token ID for refresh token
        token_id = generate_uuid()

        # Create tokens
        access_token = JWTHandler.create_access_token(user_id)
        refresh_token = JWTHandler.create_refresh_token(user_id, token_id)

        # Calculate expiry
        expires_at = datetime.now(UTC) + timedelta(days=self._settings.refresh_token_expire_days)

        # Store refresh token
        await self._token_repo.create(
            user_id=user_id,
            token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self._settings.access_token_expire_minutes * 60,
        }
