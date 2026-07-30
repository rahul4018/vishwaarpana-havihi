from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.enums.booking_status import BookingStatus


class CreateBookingRequest(BaseModel):
    temple_id: UUID
    pooja_id: UUID
    booking_date: date
    booking_time: time
    participants: int
    devotee_name: str
    devotee_mobile: str
    devotee_email: EmailStr
    special_notes: Optional[str] = None


class UpdateBookingRequest(BaseModel):
    booking_date: Optional[date] = None
    booking_time: Optional[time] = None
    participants: Optional[int] = None
    devotee_name: Optional[str] = None
    devotee_mobile: Optional[str] = None
    devotee_email: Optional[EmailStr] = None
    special_notes: Optional[str] = None

    # Workflow changes should happen through the workflow API,
    # not the generic booking update endpoint.
    booking_status: Optional[BookingStatus] = None

    payment_status: Optional[str] = None


class BookingResponse(BaseModel):
    id: UUID
    booking_number: str

    user_id: UUID
    temple_id: UUID
    pooja_id: UUID

    booking_date: date
    booking_time: time

    participants: int

    devotee_name: str
    devotee_mobile: str
    devotee_email: EmailStr

    special_notes: Optional[str] = None

    booking_status: BookingStatus
    payment_status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)