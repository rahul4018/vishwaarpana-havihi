from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateNotificationRequest(BaseModel):
    """
    Schema for creating a notification.
    """

    user_id: UUID
    title: str
    message: str
    notification_type: str = "GENERAL"
    reference_id: str | None = None


class UpdateNotificationRequest(BaseModel):
    """
    Schema for updating a notification.
    """

    title: str | None = None
    message: str | None = None
    notification_type: str | None = None
    reference_id: str | None = None
    is_read: bool | None = None


class NotificationResponse(BaseModel):
    """
    Schema returned for notification records.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    user_id: UUID
    title: str
    message: str
    notification_type: str
    reference_id: str | None
    is_read: bool
    created_at: datetime
    updated_at: datetime