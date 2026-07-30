from __future__ import annotations

import uuid
from datetime import date, datetime, time

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.booking_status import BookingStatus
from app.db.base import Base


class Booking(Base):
    """
    Booking entity.
    """

    __tablename__ = "booking"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    booking_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    temple_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("temple.id", ondelete="CASCADE"),
        nullable=False,
    )

    pooja_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pooja.id", ondelete="RESTRICT"),
        nullable=False,
    )

    booking_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    booking_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    participants: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    devotee_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    devotee_mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    devotee_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    special_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    booking_status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            name="booking_status_enum",
            native_enum=True,
            create_type=False,
        ),
        default=BookingStatus.REQUESTED,
        nullable=False,
    )

    payment_status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        lazy="joined",
    )

    temple = relationship(
        "Temple",
        lazy="joined",
    )

    pooja = relationship(
        "Pooja",
        lazy="joined",
    )

    status_history = relationship(
        "BookingStatusHistory",
        back_populates="booking",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    quotation = relationship(
        "BookingQuotation",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
    )

    priest_assignment = relationship(
        "PriestAssignment",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
    )