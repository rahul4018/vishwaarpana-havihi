from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateConsultationRequest(BaseModel):
    """
    Request schema for booking a new audio/video consultation.
    """

    priest_id: UUID | None = None
    kundli_id: UUID | None = None

    consultation_type: str = Field(
        default="VIDEO",
        min_length=3,
        max_length=30,
        examples=["VIDEO"],
    )

    scheduled_at: datetime

    duration_minutes: int = Field(
        default=30,
        ge=5,
        le=180,
    )

    topic: str | None = Field(
        default=None,
        max_length=255,
    )

    user_question: str | None = None


class UpdateConsultationRequest(BaseModel):
    """
    Request schema for users to update or reschedule
    their consultation.
    """

    priest_id: UUID | None = None
    kundli_id: UUID | None = None

    consultation_type: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
    )

    scheduled_at: datetime | None = None

    duration_minutes: int | None = Field(
        default=None,
        ge=5,
        le=180,
    )

    topic: str | None = Field(
        default=None,
        max_length=255,
    )

    user_question: str | None = None


class ManageConsultationRequest(BaseModel):
    """
    Request schema for administrators to manage
    consultation sessions.
    """

    priest_id: UUID | None = None

    consultation_status: str | None = Field(
        default=None,
        max_length=30,
    )

    consultation_fee: Decimal | None = Field(
        default=None,
        ge=0,
    )

    meeting_url: str | None = Field(
        default=None,
        max_length=1000,
    )

    meeting_id: str | None = Field(
        default=None,
        max_length=255,
    )

    admin_notes: str | None = None

    priest_notes: str | None = None

    started_at: datetime | None = None
    ended_at: datetime | None = None


class ConsultationResponse(BaseModel):
    """
    Response schema for consultation details.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    user_id: UUID
    priest_id: UUID | None
    kundli_id: UUID | None

    consultation_type: str
    consultation_status: str

    scheduled_at: datetime
    duration_minutes: int
    consultation_fee: Decimal

    topic: str | None
    user_question: str | None

    meeting_url: str | None
    meeting_id: str | None

    admin_notes: str | None
    priest_notes: str | None

    started_at: datetime | None
    ended_at: datetime | None

    created_at: datetime
    updated_at: datetime