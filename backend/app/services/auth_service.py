from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    DuplicateEmailError,
    RoleNotFoundError,
)
from app.core.security import hash_password
from app.db.models.user import User
from app.repositories import RoleRepository, UserRepository
from app.schemas import RegisterRequest, RegisterResponse


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