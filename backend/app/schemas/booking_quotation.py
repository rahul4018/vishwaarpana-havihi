from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums.quotation_status import QuotationStatus


class CreateBookingQuotationRequest(BaseModel):
    """
    Request schema for creating a booking quotation.
    """

    booking_id: UUID

    priest_cost: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    material_cost: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    catering_cost: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    transport_cost: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    miscellaneous_cost: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    discount: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    tax: Decimal = Field(
        default=0,
        ge=0,
        decimal_places=2,
    )

    advance_amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
    )

    notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    valid_until: datetime | None = None


class UpdateBookingQuotationRequest(BaseModel):
    """
    Request schema for updating a booking quotation.
    """

    priest_cost: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    material_cost: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    catering_cost: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    transport_cost: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    miscellaneous_cost: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    discount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    tax: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    advance_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    quotation_status: QuotationStatus | None = None

    accepted_at: datetime | None = None

    valid_until: datetime | None = None


class BookingQuotationResponse(BaseModel):
    """
    Response schema for booking quotation.
    """

    id: UUID

    booking_id: UUID

    quotation_number: str

    priest_cost: Decimal

    material_cost: Decimal

    catering_cost: Decimal

    transport_cost: Decimal

    miscellaneous_cost: Decimal

    discount: Decimal

    tax: Decimal

    total_amount: Decimal

    advance_amount: Decimal

    remaining_amount: Decimal

    notes: str | None

    quotation_status: QuotationStatus

    accepted_at: datetime | None

    valid_until: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )