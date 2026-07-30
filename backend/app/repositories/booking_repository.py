from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.booking import Booking


class BookingRepository:
    """
    Repository for Booking database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        booking_id: str,
    ) -> Booking | None:
        statement = select(Booking).where(
            Booking.id == booking_id,
        )
        return self.db.scalar(statement)

    def get_by_booking_number(
        self,
        booking_number: str,
    ) -> Booking | None:
        statement = select(Booking).where(
            Booking.booking_number == booking_number,
        )
        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Booking]:
        statement = (
            select(Booking)
            .order_by(Booking.created_at.desc())
        )
        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        booking: Booking,
    ) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update(
        self,
        booking: Booking,
    ) -> Booking:
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def delete(
        self,
        booking: Booking,
    ) -> None:
        self.db.delete(booking)
        self.db.commit()