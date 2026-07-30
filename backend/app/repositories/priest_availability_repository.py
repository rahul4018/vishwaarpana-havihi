from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.priest_availability import PriestAvailability


class PriestAvailabilityRepository:
    """
    Repository for Priest Availability.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        availability: PriestAvailability,
    ) -> PriestAvailability:
        self.db.add(availability)
        self.db.commit()
        self.db.refresh(availability)
        return availability

    def update(
        self,
        availability: PriestAvailability,
    ) -> PriestAvailability:
        self.db.commit()
        self.db.refresh(availability)
        return availability

    def delete(
        self,
        availability: PriestAvailability,
    ) -> None:
        self.db.delete(availability)
        self.db.commit()

    def get_by_id(
        self,
        availability_id: UUID,
    ) -> PriestAvailability | None:
        return (
            self.db.query(PriestAvailability)
            .filter(
                PriestAvailability.id == availability_id
            )
            .first()
        )

    def get_all(
        self,
    ) -> list[PriestAvailability]:
        return (
            self.db.query(PriestAvailability)
            .order_by(
                PriestAvailability.available_date.asc(),
                PriestAvailability.start_time.asc(),
            )
            .all()
        )

    def get_by_priest(
        self,
        priest_id: UUID,
    ) -> list[PriestAvailability]:
        return (
            self.db.query(PriestAvailability)
            .filter(
                PriestAvailability.priest_id == priest_id
            )
            .order_by(
                PriestAvailability.available_date.asc(),
                PriestAvailability.start_time.asc(),
            )
            .all()
        )

    def get_by_date(
        self,
        available_date: date,
    ) -> list[PriestAvailability]:
        return (
            self.db.query(PriestAvailability)
            .filter(
                PriestAvailability.available_date == available_date
            )
            .order_by(
                PriestAvailability.start_time.asc(),
            )
            .all()
        )

    def get_priest_schedule(
        self,
        priest_id: UUID,
        available_date: date,
    ) -> list[PriestAvailability]:
        return (
            self.db.query(PriestAvailability)
            .filter(
                PriestAvailability.priest_id == priest_id,
                PriestAvailability.available_date == available_date,
            )
            .order_by(
                PriestAvailability.start_time.asc(),
            )
            .all()
        )