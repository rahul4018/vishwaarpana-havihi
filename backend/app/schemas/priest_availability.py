from __future__ import annotations

from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreatePriestAvailabilityRequest(BaseModel):
    priest_id: UUID
    available_date: date
    start_time: time
    end_time: time
    is_available: bool = True
    remarks: str | None = Field(
        default=None,
        max_length=500,
    )


class UpdatePriestAvailabilityRequest(BaseModel):
    available_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    is_available: bool | None = None
    remarks: str | None = Field(
        default=None,
        max_length=500,
    )


class PriestAvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    priest_id: UUID
    available_date: date
    start_time: time
    end_time: time
    is_available: bool
    remarks: str | None
    created_at: datetime
    updated_at: datetime