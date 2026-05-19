"""JWT token handling utilities."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.constants.enums import TokenType
from app.core.exceptions import AuthenticationException


class TokenPayload(BaseModel):
    """JWT token payload schema."""

    sub: str  # User ID
    type: TokenType
    exp: datetime
    iat: datetime
    jti: str | None = None  # Token ID for refresh tokens


class JWTHandler:
    """Handles JWT token creation and verification."""

    @classmethod
    def create_access_token(cls, user_id: str) -> str:
        """Create a new access token for a user."""
        settings = get_settings()
        expires = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

        payload = {
            "sub": user_id,
            "type": TokenType.ACCESS,
            "exp": expires,
            "iat": datetime.now(UTC),
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @classmethod
    def create_refresh_token(cls, user_id: str, token_id: str) -> str:
        """Create a new refresh token for a user."""
        settings = get_settings()
        expires = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

        payload = {
            "sub": user_id,
            "type": TokenType.REFRESH,
            "exp": expires,
            "iat": datetime.now(UTC),
            "jti": token_id,
        }

        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @classmethod
    def decode_token(cls, token: str) -> TokenPayload:
        """Decode and validate a JWT token."""
        settings = get_settings()

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return TokenPayload(**payload)
        except JWTError as e:
            raise AuthenticationException(f"Invalid token: {e}")

    @classmethod
    def verify_access_token(cls, token: str) -> TokenPayload:
        """Verify an access token and return its payload."""
        payload = cls.decode_token(token)

        if payload.type != TokenType.ACCESS:
            raise AuthenticationException("Invalid token type")

        return payload

    @classmethod
    def verify_refresh_token(cls, token: str) -> TokenPayload:
        """Verify a refresh token and return its payload."""
        payload = cls.decode_token(token)

        if payload.type != TokenType.REFRESH:
            raise AuthenticationException("Invalid token type")

        return payload

    @classmethod
    def get_token_expiry(cls, token_type: TokenType) -> datetime:
        """Get the expiry datetime for a token type."""
        settings = get_settings()

        if token_type == TokenType.ACCESS:
            return datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
        return datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
