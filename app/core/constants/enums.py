"""Application enumerations."""

from enum import StrEnum


class TransactionType(StrEnum):
    """Transaction type enumeration."""

    INCOME = "income"
    EXPENSE = "expense"


class TokenType(StrEnum):
    """Token type enumeration."""

    ACCESS = "access"
    REFRESH = "refresh"
