from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateGalleryRequest(BaseModel):
    """
    Schema for creating a gallery item.
    """

    temple_id: UUID | None = None
    pooja_id: UUID | None = None
    title: str
    description: str | None = None
    image_url: str
    display_order: int = 0
    is_active: bool = True


class UpdateGalleryRequest(BaseModel):
    """
    Schema for updating a gallery item.
    """

    temple_id: UUID | None = None
    pooja_id: UUID | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class GalleryResponse(BaseModel):
    """
    Schema returned for gallery items.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    temple_id: UUID | None
    pooja_id: UUID | None
    title: str
    description: str | None
    image_url: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime