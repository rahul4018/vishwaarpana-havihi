from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateCateringRequest(BaseModel):
    """
    Request schema for creating a catering or prasadam service.
    """

    temple_id: UUID | None = None
    pooja_id: UUID | None = None

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    service_type: str = Field(
        default="CATERING",
        max_length=30,
    )

    description: str | None = None
    menu_details: str | None = None

    price_per_person: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
    )

    minimum_people: int = Field(
        default=1,
        ge=1,
    )

    maximum_people: int | None = Field(
        default=None,
        ge=1,
    )

    is_vegetarian: bool = True
    is_available: bool = True

    image_url: str | None = Field(
        default=None,
        max_length=500,
    )


class UpdateCateringRequest(BaseModel):
    """
    Request schema for updating a catering or prasadam service.
    """

    temple_id: UUID | None = None
    pooja_id: UUID | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    service_type: str | None = Field(
        default=None,
        max_length=30,
    )

    description: str | None = None
    menu_details: str | None = None

    price_per_person: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    minimum_people: int | None = Field(
        default=None,
        ge=1,
    )

    maximum_people: int | None = Field(
        default=None,
        ge=1,
    )

    is_vegetarian: bool | None = None
    is_available: bool | None = None

    image_url: str | None = Field(
        default=None,
        max_length=500,
    )


class CateringResponse(BaseModel):
    """
    Response schema for catering and prasadam services.
    """

    id: UUID

    temple_id: UUID | None
    pooja_id: UUID | None

    name: str
    service_type: str

    description: str | None
    menu_details: str | None

    price_per_person: Decimal

    minimum_people: int
    maximum_people: int | None

    is_vegetarian: bool
    is_available: bool

    image_url: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )