from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.booking_status import BookingStatus
from app.db.base import Base


class BookingStatusHistory(Base):
    """
    Stores the complete lifecycle of a booking.
    Every status change is recorded here.
    """

    __tablename__ = "booking_status_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("booking.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[BookingStatus] = mapped_column(
    Enum(
        BookingStatus,
        name="booking_status_enum",
        create_type=False,
        native_enum=True,
    ),
    nullable=False,
)

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    updated_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    booking = relationship(
        "Booking",
        back_populates="status_history",
    )