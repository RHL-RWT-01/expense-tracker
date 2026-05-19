"""Authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.dependencies import (
    get_auth_service,
    get_current_active_user,
)
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.base import ResponseSchema
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=ResponseSchema[UserResponse],
    status_code=201,
    summary="Register a new user",
    description="Create a new user account with email and password.",
)
async def register(
    data: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema[UserResponse]:
    """Register a new user."""
    user = await auth_service.register(
        name=data.name,
        email=data.email,
        password=data.password,
    )

    return ResponseSchema(
        success=True,
        message="User registered successfully",
        data=UserResponse(**user),
    )


@router.post(
    "/login",
    response_model=ResponseSchema[TokenResponse],
    summary="Login user",
    description="Authenticate user and return access and refresh tokens.",
)
async def login(
    data: LoginRequest,
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema[TokenResponse]:
    """Login user and return tokens."""
    # Get device info from user agent
    device_info = request.headers.get("User-Agent", "Unknown")

    result = await auth_service.login(
        email=data.email,
        password=data.password,
        device_info=device_info,
    )

    return ResponseSchema(
        success=True,
        message="Login successful",
        data=TokenResponse(**result["tokens"]),
    )


@router.post(
    "/refresh",
    response_model=ResponseSchema[TokenResponse],
    summary="Refresh tokens",
    description="Get new access and refresh tokens using a valid refresh token.",
)
async def refresh_tokens(
    data: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema[TokenResponse]:
    """Refresh access and refresh tokens."""
    tokens = await auth_service.refresh_tokens(data.refresh_token)

    return ResponseSchema(
        success=True,
        message="Tokens refreshed successfully",
        data=TokenResponse(**tokens),
    )


@router.post(
    "/logout",
    response_model=ResponseSchema,
    summary="Logout user",
    description="Invalidate the current refresh token.",
)
async def logout(
    data: RefreshTokenRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema:
    """Logout user by invalidating refresh token."""
    await auth_service.logout(data.refresh_token)

    return ResponseSchema(
        success=True,
        message="Logged out successfully",
    )


@router.post(
    "/logout-all",
    response_model=ResponseSchema,
    summary="Logout from all sessions",
    description="Invalidate all refresh tokens for the current user.",
)
async def logout_all(
    current_user: Annotated[dict, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema:
    """Logout user from all sessions."""
    count = await auth_service.logout_all(current_user["id"])

    return ResponseSchema(
        success=True,
        message=f"Logged out from {count} session(s)",
    )


@router.get(
    "/me",
    response_model=ResponseSchema[UserResponse],
    summary="Get current user",
    description="Get the profile of the currently authenticated user.",
)
async def get_me(
    current_user: Annotated[dict, Depends(get_current_active_user)],
) -> ResponseSchema[UserResponse]:
    """Get current user profile."""
    return ResponseSchema(
        success=True,
        message="User retrieved successfully",
        data=UserResponse(**current_user),
    )


@router.patch(
    "/change-password",
    response_model=ResponseSchema,
    summary="Change password",
    description="Change the password for the current user.",
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: Annotated[dict, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> ResponseSchema:
    """Change user password."""
    await auth_service.change_password(
        user_id=current_user["id"],
        current_password=data.current_password,
        new_password=data.new_password,
    )

    return ResponseSchema(
        success=True,
        message="Password changed successfully",
    )
