from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.kundli import Kundli


class KundliRepository:
    """
    Repository for Kundli and astrology request database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Kundli]:
        return (
            self.db.query(Kundli)
            .order_by(Kundli.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        kundli_id: UUID,
    ) -> Kundli | None:
        return (
            self.db.query(Kundli)
            .filter(Kundli.id == kundli_id)
            .first()
        )

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Kundli]:
        return (
            self.db.query(Kundli)
            .filter(Kundli.user_id == user_id)
            .order_by(Kundli.created_at.desc())
            .all()
        )

    def get_by_priest_id(
        self,
        priest_id: UUID,
    ) -> list[Kundli]:
        return (
            self.db.query(Kundli)
            .filter(Kundli.priest_id == priest_id)
            .order_by(Kundli.created_at.desc())
            .all()
        )

    def get_by_status(
        self,
        request_status: str,
    ) -> list[Kundli]:
        return (
            self.db.query(Kundli)
            .filter(
                Kundli.request_status
                == request_status.upper()
            )
            .order_by(Kundli.created_at.desc())
            .all()
        )

    def create(
        self,
        kundli: Kundli,
    ) -> Kundli:
        self.db.add(kundli)
        self.db.commit()
        self.db.refresh(kundli)

        return kundli

    def update(
        self,
        kundli: Kundli,
    ) -> Kundli:
        self.db.commit()
        self.db.refresh(kundli)

        return kundli

    def delete(
        self,
        kundli: Kundli,
    ) -> None:
        self.db.delete(kundli)
        self.db.commit()