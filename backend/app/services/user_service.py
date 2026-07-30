from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    BadRequestError,
    ResourceNotFoundError,
)
from app.core.security import hash_password
from app.db.models.user import User
from app.repositories import (
    RoleRepository,
    UserRepository,
)
from app.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)


class UserService:
    """
    User business logic.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def create(
        self,
        request: CreateUserRequest,
    ) -> UserResponse:
        existing_user = self.user_repository.get_by_email(
            request.email,
        )

        if existing_user is not None:
            raise BadRequestError(
                "User with this email already exists."
            )

        role = self.role_repository.get_by_id(
            str(request.role_id),
        )

        if role is None:
            raise ResourceNotFoundError(
                "Role not found."
            )

        user = User(
            full_name=request.full_name,
            email=request.email,
            mobile=request.mobile,
            password_hash=hash_password(
                request.password,
            ),
            role_id=request.role_id,
            is_active=True,
            is_verified=False,
        )

        created = self.user_repository.create(user)

        return UserResponse(
            id=created.id,
            full_name=created.full_name,
            email=created.email,
            mobile=created.mobile,
            role=created.role.name,
            is_active=created.is_active,
            is_verified=created.is_verified,
            created_at=created.created_at,
            updated_at=created.updated_at,
        )

    def get_by_id(
        self,
        user_id: str,
    ) -> UserResponse:
        user = self.user_repository.get_by_id(
            user_id,
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found."
            )

        return UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            mobile=user.mobile,
            role=user.role.name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def get_all(
        self,
    ) -> list[UserResponse]:
        users = self.user_repository.get_all()

        return [
            UserResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                mobile=user.mobile,
                role=user.role.name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    def update(
        self,
        user_id: str,
        request: UpdateUserRequest,
    ) -> UserResponse:
        user = self.user_repository.get_by_id(
            user_id,
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found."
            )

        if request.role_id is not None:
            role = self.role_repository.get_by_id(
                str(request.role_id),
            )

            if role is None:
                raise ResourceNotFoundError(
                    "Role not found."
                )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(user, field, value)

        updated = self.user_repository.update(user)

        return UserResponse(
            id=updated.id,
            full_name=updated.full_name,
            email=updated.email,
            mobile=updated.mobile,
            role=updated.role.name,
            is_active=updated.is_active,
            is_verified=updated.is_verified,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )

    def delete(
        self,
        user_id: str,
    ) -> None:
        user = self.user_repository.get_by_id(
            user_id,
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found."
            )

        self.user_repository.delete(user)