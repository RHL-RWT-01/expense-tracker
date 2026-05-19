"""General utility helper functions."""

import uuid
from typing import Any

from bson import ObjectId

from app.core.exceptions import ValidationException


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def to_objectid(id_str: str) -> ObjectId:
    """Convert a string to MongoDB ObjectId."""
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValidationException(f"Invalid ID format: {id_str}")


def from_objectid(obj: Any) -> str:
    """Convert MongoDB ObjectId to string."""
    if isinstance(obj, ObjectId):
        return str(obj)
    return str(obj)


def serialize_doc(doc: dict[str, Any] | None) -> dict[str, Any] | None:
    """Serialize a MongoDB document, converting ObjectId to string."""
    if doc is None:
        return None

    result = {}
    for key, value in doc.items():
        if key == "_id":
            result["id"] = from_objectid(value)
        elif isinstance(value, ObjectId):
            result[key] = from_objectid(value)
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        elif isinstance(value, list):
            result[key] = [
                serialize_doc(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            result[key] = value

    return result
