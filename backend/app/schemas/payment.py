from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreatePaymentRequest(BaseModel):
    """
    Request schema for creating a payment.
    """

    booking_id: UUID

    amount: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
    )

    payment_method: str | None = Field(
        default=None,
        max_length=50,
    )

    gateway: str | None = Field(
        default=None,
        max_length=50,
    )


class UpdatePaymentRequest(BaseModel):
    """
    Request schema for updating payment details/status.
    """

    transaction_id: str | None = Field(
        default=None,
        max_length=150,
    )

    payment_method: str | None = Field(
        default=None,
        max_length=50,
    )

    payment_status: str | None = Field(
        default=None,
        max_length=30,
    )

    gateway: str | None = Field(
        default=None,
        max_length=50,
    )

    gateway_payment_id: str | None = Field(
        default=None,
        max_length=150,
    )

    failure_reason: str | None = None

    paid_at: datetime | None = None


class PaymentResponse(BaseModel):
    """
    Response schema for payment data.
    """

    id: UUID
    booking_id: UUID

    transaction_id: str | None

    amount: Decimal

    payment_method: str | None
    payment_status: str

    gateway: str | None
    gateway_payment_id: str | None

    failure_reason: str | None
    paid_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )