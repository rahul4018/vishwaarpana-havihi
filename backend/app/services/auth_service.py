from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    DuplicateEmailError,
    InvalidCredentialsError,
    RoleNotFoundError,
)
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.core.security import (
    hash_password,
    verify_password,
)
from app.db.models.user import User
from app.repositories import RoleRepository, UserRepository
from app.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def register(self, request: RegisterRequest) -> RegisterResponse:
        """
        Register a new user with the default DEVOTEE role.
        """
        existing_user = self.user_repository.get_by_email(
            str(request.email)
        )

        if existing_user is not None:
            raise DuplicateEmailError(
                "Email is already registered."
            )

        role = self.role_repository.get_by_name("DEVOTEE")

        if role is None:
            raise RoleNotFoundError(
                "Default role 'DEVOTEE' does not exist."
            )

        user = User(
            full_name=request.full_name,
            email=str(request.email),
            mobile=request.mobile,
            password_hash=hash_password(request.password),
            role_id=role.id,
            is_active=True,
            is_verified=False,
        )

        created_user = self.user_repository.create(user)

        return RegisterResponse(
            id=str(created_user.id),
            full_name=created_user.full_name,
            email=created_user.email,
            role=role.name,
        )

    def login(self, request: LoginRequest) -> LoginResponse:
        """
        Authenticate a user and return JWT access and refresh tokens.
        """
        user = self.user_repository.get_by_email(
            str(request.email)
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise InvalidCredentialsError(
                "User account is inactive."
            )

        access_token = create_access_token(
            subject=str(user.email),
        )

        refresh_token = create_refresh_token(
            subject=str(user.email),
        )

        return LoginResponse(
            user=RegisterResponse(
                id=str(user.id),
                full_name=user.full_name,
                email=user.email,
                role=user.role.name,
            ),
            tokens=TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
        )