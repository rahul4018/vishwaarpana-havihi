from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreatePoojaRequest(BaseModel):
    """
    Request schema for creating a pooja.
    """

    temple_id: str
    category_id: str
    priest_id: str | None = None

    name: str = Field(
        min_length=2,
        max_length=255,
    )

    slug: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = None

    duration_minutes: int = Field(
        default=60,
        ge=1,
    )

    price: Decimal = Field(
        gt=0,
    )

    max_participants: int = Field(
        default=1,
        ge=1,
    )

    online_booking: bool = True

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class UpdatePoojaRequest(BaseModel):
    """
    Request schema for updating a pooja.
    """

    category_id: str | None = None
    priest_id: str | None = None

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    slug: str | None = Field(
        default=None,
        max_length=255,
    )

    description: str | None = None

    duration_minutes: int | None = Field(
        default=None,
        ge=1,
    )

    price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    max_participants: int | None = Field(
        default=None,
        ge=1,
    )

    online_booking: bool | None = None

    is_active: bool | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class PoojaResponse(BaseModel):
    """
    Pooja response schema.
    """

    id: UUID
    temple_id: UUID
    category_id: UUID
    priest_id: UUID | None

    name: str
    slug: str
    description: str | None

    duration_minutes: int
    price: Decimal
    max_participants: int

    online_booking: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )