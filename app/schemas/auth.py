"""Authentication schemas."""

import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.constants.defaults import MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH


class RegisterRequest(BaseModel):
    """User registration request schema."""

    name: Annotated[str, Field(min_length=2, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)]

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean name."""
        return v.strip()


class LoginRequest(BaseModel):
    """User login request schema."""

    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until access token expires


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""

    current_password: str
    new_password: Annotated[
        str, Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
    ]

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v
