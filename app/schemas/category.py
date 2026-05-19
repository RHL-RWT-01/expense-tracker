"""Category schemas."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class CategoryCreate(BaseModel):
    """Category creation request schema."""

    name: Annotated[str, Field(min_length=1, max_length=50)]


class CategoryUpdate(BaseModel):
    """Category update request schema."""

    name: Annotated[str | None, Field(min_length=1, max_length=50)] = None


class CategoryResponse(BaseSchema):
    """Category response schema."""

    id: str
    name: str
    user_id: str | None = None
    is_default: bool
    created_at: datetime
