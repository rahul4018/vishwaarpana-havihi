from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.consultation import Consultation


class ConsultationRepository:
    """
    Repository for Consultation database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .order_by(Consultation.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        consultation_id: UUID,
    ) -> Consultation | None:
        return (
            self.db.query(Consultation)
            .filter(Consultation.id == consultation_id)
            .first()
        )

    def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .filter(Consultation.user_id == user_id)
            .order_by(Consultation.scheduled_at.desc())
            .all()
        )

    def get_by_priest_id(
        self,
        priest_id: UUID,
    ) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .filter(Consultation.priest_id == priest_id)
            .order_by(Consultation.scheduled_at.desc())
            .all()
        )

    def get_by_kundli_id(
        self,
        kundli_id: UUID,
    ) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .filter(Consultation.kundli_id == kundli_id)
            .order_by(Consultation.created_at.desc())
            .all()
        )

    def get_by_status(
        self,
        consultation_status: str,
    ) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .filter(
                Consultation.consultation_status
                == consultation_status
            )
            .order_by(Consultation.scheduled_at.desc())
            .all()
        )

    def get_by_type(
        self,
        consultation_type: str,
    ) -> list[Consultation]:
        return (
            self.db.query(Consultation)
            .filter(
                Consultation.consultation_type
                == consultation_type
            )
            .order_by(Consultation.scheduled_at.desc())
            .all()
        )

    def create(
        self,
        consultation: Consultation,
    ) -> Consultation:
        self.db.add(consultation)
        self.db.commit()
        self.db.refresh(consultation)

        return consultation

    def update(
        self,
        consultation: Consultation,
    ) -> Consultation:
        self.db.add(consultation)
        self.db.commit()
        self.db.refresh(consultation)

        return consultation

    def delete(
        self,
        consultation: Consultation,
    ) -> None:
        self.db.delete(consultation)
        self.db.commit()