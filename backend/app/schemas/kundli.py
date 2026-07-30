from __future__ import annotations

from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateKundliRequest(BaseModel):
    """
    Request schema for creating a Kundli or astrology request.
    The authenticated user's ID will be taken from the access token.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
    )

    date_of_birth: date

    time_of_birth: time

    place_of_birth: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    gender: str | None = Field(
        default=None,
        max_length=30,
    )

    service_type: str = Field(
        default="KUNDLI",
        max_length=50,
    )

    user_question: str | None = None


class UpdateKundliRequest(BaseModel):
    """
    Request schema allowing users to update
    their own Kundli request details.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    date_of_birth: date | None = None

    time_of_birth: time | None = None

    place_of_birth: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    gender: str | None = Field(
        default=None,
        max_length=30,
    )

    service_type: str | None = Field(
        default=None,
        max_length=50,
    )

    user_question: str | None = None


class ManageKundliRequest(BaseModel):
    """
    Admin schema for managing a Kundli request.
    """

    priest_id: UUID | None = None

    request_status: str | None = Field(
        default=None,
        max_length=30,
    )

    report_url: str | None = Field(
        default=None,
        max_length=500,
    )

    admin_notes: str | None = None


class KundliResponse(BaseModel):
    """
    Response schema for Kundli and astrology requests.
    """

    id: UUID
    user_id: UUID
    priest_id: UUID | None

    full_name: str
    date_of_birth: date
    time_of_birth: time
    place_of_birth: str

    gender: str | None

    service_type: str
    request_status: str

    user_question: str | None

    report_url: str | None
    admin_notes: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )