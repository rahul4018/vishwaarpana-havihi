from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateInvoiceRequest(BaseModel):
    """
    Request schema for creating an invoice.
    """

    booking_id: UUID
    payment_id: UUID | None = None

    subtotal: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
    )

    tax_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
    )

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        decimal_places=2,
    )

    notes: str | None = None


class UpdateInvoiceRequest(BaseModel):
    """
    Request schema for updating an invoice.
    """

    payment_id: UUID | None = None

    subtotal: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    tax_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    discount_amount: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    invoice_status: str | None = Field(
        default=None,
        max_length=30,
    )

    notes: str | None = None


class InvoiceResponse(BaseModel):
    """
    Response schema for invoice data.
    """

    id: UUID
    invoice_number: str

    booking_id: UUID
    payment_id: UUID | None

    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal

    invoice_status: str
    notes: str | None

    issued_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )