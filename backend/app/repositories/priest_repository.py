from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.priest import Priest


class PriestRepository:
    """
    Repository for Priest database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        priest_id: str,
    ) -> Priest | None:
        statement = select(Priest).where(
            Priest.id == priest_id,
        )
        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> Priest | None:
        statement = select(Priest).where(
            Priest.email == email,
        )
        return self.db.scalar(statement)

    def get_by_phone(
        self,
        phone: str,
    ) -> Priest | None:
        statement = select(Priest).where(
            Priest.phone == phone,
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Priest]:
        statement = (
            select(Priest)
            .order_by(Priest.full_name.asc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        priest: Priest,
    ) -> Priest:
        self.db.add(priest)
        self.db.commit()
        self.db.refresh(priest)
        return priest

    def update(
        self,
        priest: Priest,
    ) -> Priest:
        self.db.commit()
        self.db.refresh(priest)
        return priest

    def delete(
        self,
        priest: Priest,
    ) -> None:
        self.db.delete(priest)
        self.db.commit()