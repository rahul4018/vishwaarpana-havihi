from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateReviewRequest(BaseModel):
    """
    Schema for creating a review.
    """

    booking_id: UUID
    pooja_id: UUID

    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    review_text: str | None = None


class UpdateReviewRequest(BaseModel):
    """
    Schema for updating a review.
    """

    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    review_text: str | None = None


class ModerateReviewRequest(BaseModel):
    """
    Schema for admin review moderation.
    """

    review_status: str
    admin_response: str | None = None


class ReviewResponse(BaseModel):
    """
    Schema returned for review records.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    user_id: UUID
    booking_id: UUID
    pooja_id: UUID
    rating: int
    review_text: str | None
    review_status: str
    admin_response: str | None
    created_at: datetime
    updated_at: datetime