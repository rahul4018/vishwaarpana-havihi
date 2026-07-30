from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.priest_assignment import PriestAssignment


class PriestAssignmentRepository:
    """
    Repository for PriestAssignment database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_by_id(
        self,
        assignment_id: str,
    ) -> PriestAssignment | None:
        statement = select(
            PriestAssignment
        ).where(
            PriestAssignment.id == assignment_id,
        )

        return self.db.scalar(statement)

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> PriestAssignment | None:
        statement = select(
            PriestAssignment
        ).where(
            PriestAssignment.booking_id == booking_id,
        )

        return self.db.scalar(statement)

    def get_by_priest_id(
        self,
        priest_id: str,
    ) -> list[PriestAssignment]:
        statement = (
            select(PriestAssignment)
            .where(
                PriestAssignment.priest_id == priest_id,
            )
            .order_by(
                PriestAssignment.assigned_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_all(
        self,
    ) -> list[PriestAssignment]:
        statement = (
            select(PriestAssignment)
            .order_by(
                PriestAssignment.assigned_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        assignment: PriestAssignment,
    ) -> PriestAssignment:
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def update(
        self,
        assignment: PriestAssignment,
    ) -> PriestAssignment:
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def delete(
        self,
        assignment: PriestAssignment,
    ) -> None:
        self.db.delete(assignment)
        self.db.commit()