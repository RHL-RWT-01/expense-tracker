"""Category routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_category_service, get_current_active_user
from app.schemas.base import ResponseSchema
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=ResponseSchema[list[CategoryResponse]],
    summary="List categories",
    description="List all categories available to the current user (defaults + custom).",
)
async def list_categories(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ResponseSchema[list[CategoryResponse]]:
    """List all categories for the user."""
    categories = await category_service.list_categories(current_user["id"])

    return ResponseSchema(
        success=True,
        message="Categories retrieved successfully",
        data=[CategoryResponse(**c) for c in categories],
    )


@router.post(
    "",
    response_model=ResponseSchema[CategoryResponse],
    status_code=201,
    summary="Create category",
    description="Create a new custom category.",
)
async def create_category(
    data: CategoryCreate,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ResponseSchema[CategoryResponse]:
    """Create a new custom category."""
    category = await category_service.create_category(
        user_id=current_user["id"],
        name=data.name,
    )

    return ResponseSchema(
        success=True,
        message="Category created successfully",
        data=CategoryResponse(**category),
    )


@router.patch(
    "/{category_id}",
    response_model=ResponseSchema[CategoryResponse],
    summary="Update category",
    description="Update a custom category (cannot update default categories).",
)
async def update_category(
    category_id: str,
    data: CategoryUpdate,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ResponseSchema[CategoryResponse]:
    """Update a custom category."""
    category = await category_service.update_category(
        category_id=category_id,
        user_id=current_user["id"],
        update_data=data.model_dump(exclude_unset=True),
    )

    return ResponseSchema(
        success=True,
        message="Category updated successfully",
        data=CategoryResponse(**category),
    )


@router.delete(
    "/{category_id}",
    response_model=ResponseSchema,
    summary="Delete category",
    description="Delete a custom category (cannot delete default categories or categories in use).",
)
async def delete_category(
    category_id: str,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ResponseSchema:
    """Delete a custom category."""
    await category_service.delete_category(
        category_id=category_id,
        user_id=current_user["id"],
    )

    return ResponseSchema(
        success=True,
        message="Category deleted successfully",
    )
