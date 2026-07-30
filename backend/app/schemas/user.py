from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str | None = None
    password: str
    role_id: UUID


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    mobile: str | None = None
    role_id: UUID | None = None
    is_active: bool | None = None
    is_verified: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    mobile: str |None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserListResponse(BaseModel):
    users: list[UserResponse]