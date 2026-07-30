from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.catering import Catering


class CateringRepository:
    """
    Repository for catering and prasadam database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Catering]:
        return (
            self.db.query(Catering)
            .order_by(Catering.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        catering_id: UUID,
    ) -> Catering | None:
        return (
            self.db.query(Catering)
            .filter(Catering.id == catering_id)
            .first()
        )

    def get_by_temple_id(
        self,
        temple_id: UUID,
    ) -> list[Catering]:
        return (
            self.db.query(Catering)
            .filter(Catering.temple_id == temple_id)
            .order_by(Catering.created_at.desc())
            .all()
        )

    def get_by_pooja_id(
        self,
        pooja_id: UUID,
    ) -> list[Catering]:
        return (
            self.db.query(Catering)
            .filter(Catering.pooja_id == pooja_id)
            .order_by(Catering.created_at.desc())
            .all()
        )

    def get_by_service_type(
        self,
        service_type: str,
    ) -> list[Catering]:
        return (
            self.db.query(Catering)
            .filter(
                Catering.service_type
                == service_type.upper()
            )
            .order_by(Catering.created_at.desc())
            .all()
        )

    def get_available(self) -> list[Catering]:
        return (
            self.db.query(Catering)
            .filter(Catering.is_available.is_(True))
            .order_by(Catering.created_at.desc())
            .all()
        )

    def create(
        self,
        catering: Catering,
    ) -> Catering:
        self.db.add(catering)
        self.db.commit()
        self.db.refresh(catering)

        return catering

    def update(
        self,
        catering: Catering,
    ) -> Catering:
        self.db.commit()
        self.db.refresh(catering)

        return catering

    def delete(
        self,
        catering: Catering,
    ) -> None:
        self.db.delete(catering)
        self.db.commit()