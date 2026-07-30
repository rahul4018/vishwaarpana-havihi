from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.invoice import Invoice


class InvoiceRepository:
    """
    Repository for Invoice database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        invoice_id: str,
    ) -> Invoice | None:
        statement = select(Invoice).where(
            Invoice.id == invoice_id,
        )
        return self.db.scalar(statement)

    def get_by_invoice_number(
        self,
        invoice_number: str,
    ) -> Invoice | None:
        statement = select(Invoice).where(
            Invoice.invoice_number == invoice_number,
        )
        return self.db.scalar(statement)

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> list[Invoice]:
        statement = (
            select(Invoice)
            .where(Invoice.booking_id == booking_id)
            .order_by(Invoice.created_at.desc())
        )
        return list(
            self.db.scalars(statement).all()
        )

    def get_by_payment_id(
        self,
        payment_id: str,
    ) -> list[Invoice]:
        statement = (
            select(Invoice)
            .where(Invoice.payment_id == payment_id)
            .order_by(Invoice.created_at.desc())
        )
        return list(
            self.db.scalars(statement).all()
        )

    def get_all(
        self,
    ) -> list[Invoice]:
        statement = select(Invoice).order_by(
            Invoice.created_at.desc(),
        )
        return list(
            self.db.scalars(statement).all()
        )

    def count(
        self,
    ) -> int:
        return len(self.get_all())

    def create(
        self,
        invoice: Invoice,
    ) -> Invoice:
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def update(
        self,
        invoice: Invoice,
    ) -> Invoice:
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def delete(
        self,
        invoice: Invoice,
    ) -> None:
        self.db.delete(invoice)
        self.db.commit()