from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateContactRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    subject: str | None = Field(
        default=None,
        max_length=255,
    )

    message: str = Field(
        ...,
        min_length=1,
    )


class UpdateContactRequest(BaseModel):
    enquiry_status: str | None = Field(
        default=None,
        max_length=30,
    )

    admin_notes: str | None = None


class ContactResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    name: str
    email: EmailStr
    phone: str | None
    subject: str | None
    message: str
    enquiry_status: str
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime