from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.payment import Payment


class PaymentRepository:
    """
    Repository for Payment database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        payment_id: str,
    ) -> Payment | None:
        statement = select(Payment).where(
            Payment.id == payment_id,
        )
        return self.db.scalar(statement)

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> list[Payment]:
        statement = (
            select(Payment)
            .where(Payment.booking_id == booking_id)
            .order_by(Payment.created_at.desc())
        )
        return list(
            self.db.scalars(statement).all()
        )

    def get_by_transaction_id(
        self,
        transaction_id: str,
    ) -> Payment | None:
        statement = select(Payment).where(
            Payment.transaction_id == transaction_id,
        )
        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Payment]:
        statement = select(Payment).order_by(
            Payment.created_at.desc(),
        )
        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        payment: Payment,
    ) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update(
        self,
        payment: Payment,
    ) -> Payment:
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete(
        self,
        payment: Payment,
    ) -> None:
        self.db.delete(payment)
        self.db.commit()