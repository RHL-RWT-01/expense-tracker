"""Common validation utilities."""

from datetime import datetime

from bson import ObjectId

from app.core.exceptions import ValidationException


def validate_object_id(id_value: str, field_name: str = "id") -> str:
    """Validate that a string is a valid MongoDB ObjectId."""
    if not ObjectId.is_valid(id_value):
        raise ValidationException(
            message=f"Invalid {field_name} format",
            errors=[{"field": field_name, "message": "Must be a valid ObjectId"}],
        )
    return id_value


def validate_date_range(
    start_date: datetime | None,
    end_date: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    """Validate that start_date is before end_date."""
    if start_date and end_date and start_date > end_date:
        raise ValidationException(
            message="Invalid date range",
            errors=[
                {
                    "field": "date_range",
                    "message": "start_date must be before end_date",
                }
            ],
        )
    return start_date, end_date
