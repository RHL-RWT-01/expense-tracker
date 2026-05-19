"""Transaction routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_active_user, get_transaction_service
from app.schemas.base import PaginatedResponse, ResponseSchema
from app.schemas.transaction import (
    TransactionCreate,
    TransactionListParams,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "",
    response_model=ResponseSchema[TransactionResponse],
    status_code=201,
    summary="Create transaction",
    description="Create a new income or expense transaction.",
)
async def create_transaction(
    data: TransactionCreate,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
) -> ResponseSchema[TransactionResponse]:
    """Create a new transaction."""
    transaction = await transaction_service.create_transaction(
        user_id=current_user["id"],
        type=data.type,
        amount=data.amount,
        category_id=data.category_id,
        transaction_date=data.transaction_date,
        note=data.note,
    )

    return ResponseSchema(
        success=True,
        message="Transaction created successfully",
        data=TransactionResponse(**transaction),
    )


@router.get(
    "",
    response_model=PaginatedResponse[TransactionResponse],
    summary="List transactions",
    description="List all transactions for the current user with filtering and pagination.",
)
async def list_transactions(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
    params: Annotated[TransactionListParams, Query()],
) -> PaginatedResponse[TransactionResponse]:
    """List transactions with filtering and pagination."""
    transactions, pagination = await transaction_service.list_transactions(
        user_id=current_user["id"],
        page=params.page,
        page_size=params.page_size,
        sort_by=params.sort_by,
        sort_order=params.sort_order,
        type=params.type,
        category_id=params.category_id,
        start_date=params.start_date,
        end_date=params.end_date,
        search=params.search,
        min_amount=params.min_amount,
        max_amount=params.max_amount,
    )

    return PaginatedResponse(
        success=True,
        message="Transactions retrieved successfully",
        data=[TransactionResponse(**t) for t in transactions],
        meta=pagination,
    )


@router.get(
    "/{transaction_id}",
    response_model=ResponseSchema[TransactionResponse],
    summary="Get transaction",
    description="Get a specific transaction by ID.",
)
async def get_transaction(
    transaction_id: str,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
) -> ResponseSchema[TransactionResponse]:
    """Get a transaction by ID."""
    transaction = await transaction_service.get_transaction(
        transaction_id=transaction_id,
        user_id=current_user["id"],
    )

    return ResponseSchema(
        success=True,
        message="Transaction retrieved successfully",
        data=TransactionResponse(**transaction),
    )


@router.patch(
    "/{transaction_id}",
    response_model=ResponseSchema[TransactionResponse],
    summary="Update transaction",
    description="Update an existing transaction.",
)
async def update_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
) -> ResponseSchema[TransactionResponse]:
    """Update a transaction."""
    transaction = await transaction_service.update_transaction(
        transaction_id=transaction_id,
        user_id=current_user["id"],
        update_data=data.model_dump(exclude_unset=True),
    )

    return ResponseSchema(
        success=True,
        message="Transaction updated successfully",
        data=TransactionResponse(**transaction),
    )


@router.delete(
    "/{transaction_id}",
    response_model=ResponseSchema,
    summary="Delete transaction",
    description="Delete a transaction (soft delete).",
)
async def delete_transaction(
    transaction_id: str,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
) -> ResponseSchema:
    """Delete a transaction."""
    await transaction_service.delete_transaction(
        transaction_id=transaction_id,
        user_id=current_user["id"],
    )

    return ResponseSchema(
        success=True,
        message="Transaction deleted successfully",
    )
