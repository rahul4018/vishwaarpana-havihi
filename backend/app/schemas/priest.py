from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreatePriestRequest(BaseModel):
    """
    Request schema for creating a priest.
    """

    temple_id: UUID

    full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr | None = None

    phone: str = Field(
        min_length=10,
        max_length=20,
    )

    experience_years: int = Field(
        default=0,
        ge=0,
    )

    specialization: str | None = None

    bio: str | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class UpdatePriestRequest(BaseModel):
    """
    Request schema for updating a priest.
    """

    full_name: str | None = Field(
        default=None,
        max_length=150,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    experience_years: int | None = Field(
        default=None,
        ge=0,
    )

    specialization: str | None = None

    bio: str | None = None

    is_active: bool | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class PriestResponse(BaseModel):
    """
    Priest response schema.
    """

    id: UUID
    temple_id: UUID
    full_name: str
    email: EmailStr | None
    phone: str
    experience_years: int
    specialization: str | None
    bio: str | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )