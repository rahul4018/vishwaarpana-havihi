from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
) -> list[UserResponse]:
    """
    Get all users.
    """
    return UserService(db).get_all()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Get user by ID.
    """
    return UserService(db).get_by_id(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Create a new user.
    """
    return UserService(db).create(request)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: str,
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Update an existing user.
    """
    return UserService(db).update(
        user_id=user_id,
        request=request,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
) -> Response:
    """
    Delete a user.
    """
    UserService(db).delete(user_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )