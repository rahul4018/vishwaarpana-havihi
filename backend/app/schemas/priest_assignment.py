from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreatePriestAssignmentRequest(BaseModel):
    booking_id: UUID
    priest_id: UUID
    assigned_by: UUID
    notes: Optional[str] = None


class UpdatePriestAssignmentRequest(BaseModel):
    priest_id: Optional[UUID] = None
    notes: Optional[str] = None
    is_confirmed: Optional[bool] = None


class PriestAssignmentResponse(BaseModel):
    id: UUID
    booking_id: UUID
    priest_id: UUID
    assigned_by: UUID
    notes: Optional[str]
    is_confirmed: bool
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)