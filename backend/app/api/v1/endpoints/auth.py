from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_admin
from app.core.exceptions.http_exceptions import (
    DuplicateEmailError,
    InvalidCredentialsError,
    InvalidTokenError,
    RoleNotFoundError,
)
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:
    """
    Register a new user with the default DEVOTEE role.
    """
    auth_service = AuthService(db)

    try:
        return auth_service.register(request)

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except RoleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate a user and return JWT access and refresh tokens.",
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user using email and password.
    """
    auth_service = AuthService(db)

    try:
        return auth_service.login(request)

    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token.",
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> RefreshTokenResponse:
    """
    Generate a new access token from a valid refresh token.
    """
    auth_service = AuthService(db)

    try:
        return auth_service.refresh_token(request)

    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Return the currently authenticated user.",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Return the profile of the authenticated user.
    """
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "role": current_user.role.name,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
    }


@router.get(
    "/admin-test",
    status_code=status.HTTP_200_OK,
    summary="Admin test endpoint",
    description="Accessible only to ADMIN and SUPER_ADMIN.",
)
def admin_test(
    current_user: User = Depends(require_admin),
) -> dict[str, str]:
    """
    Test endpoint for verifying Role-Based Access Control (RBAC).
    """
    return {
        "message": f"Welcome {current_user.full_name}",
        "role": current_user.role.name,
    }   