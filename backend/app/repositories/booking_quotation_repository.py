from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.booking_quotation import BookingQuotation


class BookingQuotationRepository:
    """
    Repository for BookingQuotation database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        quotation_id: str,
    ) -> BookingQuotation | None:
        statement = select(BookingQuotation).where(
            BookingQuotation.id == quotation_id,
        )
        return self.db.scalar(statement)

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> BookingQuotation | None:
        statement = select(BookingQuotation).where(
            BookingQuotation.booking_id == booking_id,
        )
        return self.db.scalar(statement)

    def get_by_quotation_number(
        self,
        quotation_number: str,
    ) -> BookingQuotation | None:
        statement = select(BookingQuotation).where(
            BookingQuotation.quotation_number == quotation_number,
        )
        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[BookingQuotation]:
        statement = (
            select(BookingQuotation)
            .order_by(
                BookingQuotation.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        quotation: BookingQuotation,
    ) -> BookingQuotation:
        self.db.add(quotation)
        self.db.commit()
        self.db.refresh(quotation)
        return quotation

    def update(
        self,
        quotation: BookingQuotation,
    ) -> BookingQuotation:
        self.db.commit()
        self.db.refresh(quotation)
        return quotation

    def delete(
        self,
        quotation: BookingQuotation,
    ) -> None:
        self.db.delete(quotation)
        self.db.commit()