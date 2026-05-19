"""Password hashing and verification utilities."""

from passlib.context import CryptContext


class PasswordHandler:
    """Handles password hashing and verification using bcrypt."""

    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        """Hash a plain text password."""
        return cls._context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return cls._context.verify(plain_password, hashed_password)

    @classmethod
    def needs_rehash(cls, hashed_password: str) -> bool:
        """Check if a password hash needs to be updated."""
        return cls._context.needs_update(hashed_password)
