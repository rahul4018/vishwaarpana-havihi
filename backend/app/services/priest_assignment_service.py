from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestError,
    ResourceNotFoundError,
)
from app.db.models.priest_assignment import PriestAssignment
from app.repositories.booking_repository import BookingRepository
from app.repositories.priest_assignment_repository import (
    PriestAssignmentRepository,
)
from app.repositories.priest_repository import PriestRepository
from app.schemas.priest_assignment import (
    CreatePriestAssignmentRequest,
    PriestAssignmentResponse,
    UpdatePriestAssignmentRequest,
)


class PriestAssignmentService:
    """
    Business logic for priest assignments.
    """

    def __init__(self, db: Session):
        self.db = db
        self.assignment_repository = PriestAssignmentRepository(db)
        self.booking_repository = BookingRepository(db)
        self.priest_repository = PriestRepository(db)

    def create(
        self,
        request: CreatePriestAssignmentRequest,
    ) -> PriestAssignmentResponse:

        booking = self.booking_repository.get_by_id(
            request.booking_id
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        priest = self.priest_repository.get_by_id(
            request.priest_id
        )

        if priest is None:
            raise ResourceNotFoundError(
                "Priest not found."
            )

        if not priest.is_active:
            raise BadRequestError(
                "Priest is inactive."
            )

        existing = (
            self.assignment_repository.get_by_booking_id(
                request.booking_id
            )
        )

        if existing:
            raise BadRequestError(
                "Booking already has a priest assigned."
            )

        assignment = PriestAssignment(
            booking_id=request.booking_id,
            priest_id=request.priest_id,
            assigned_by=request.assigned_by,
            notes=request.notes,
        )

        assignment = self.assignment_repository.create(
            assignment
        )

        return PriestAssignmentResponse.model_validate(
            assignment
        )

    def get_all(
        self,
    ) -> list[PriestAssignmentResponse]:

        assignments = (
            self.assignment_repository.get_all()
        )

        return [
            PriestAssignmentResponse.model_validate(a)
            for a in assignments
        ]

    def get_by_id(
        self,
        assignment_id,
    ) -> PriestAssignmentResponse:

        assignment = (
            self.assignment_repository.get_by_id(
                assignment_id
            )
        )

        if assignment is None:
            raise ResourceNotFoundError(
                "Priest assignment not found."
            )

        return PriestAssignmentResponse.model_validate(
            assignment
        )

    def get_by_booking(
        self,
        booking_id,
    ) -> PriestAssignmentResponse:

        assignment = (
            self.assignment_repository.get_by_booking_id(
                booking_id
            )
        )

        if assignment is None:
            raise ResourceNotFoundError(
                "Priest assignment not found."
            )

        return PriestAssignmentResponse.model_validate(
            assignment
        )

    def get_by_priest(
        self,
        priest_id,
    ) -> list[PriestAssignmentResponse]:

        assignments = (
            self.assignment_repository.get_by_priest_id(
                priest_id
            )
        )

        return [
            PriestAssignmentResponse.model_validate(a)
            for a in assignments
        ]

    def update(
        self,
        assignment_id,
        request: UpdatePriestAssignmentRequest,
    ) -> PriestAssignmentResponse:

        assignment = (
            self.assignment_repository.get_by_id(
                assignment_id
            )
        )

        if assignment is None:
            raise ResourceNotFoundError(
                "Priest assignment not found."
            )

        if request.priest_id is not None:

            priest = self.priest_repository.get_by_id(
                request.priest_id
            )

            if priest is None:
                raise ResourceNotFoundError(
                    "Priest not found."
                )

            if not priest.is_active:
                raise BadRequestError(
                    "Priest is inactive."
                )

            assignment.priest_id = request.priest_id

        if request.notes is not None:
            assignment.notes = request.notes

        if request.is_confirmed is not None:
            assignment.is_confirmed = (
                request.is_confirmed
            )

        assignment = (
            self.assignment_repository.update(
                assignment
            )
        )

        return PriestAssignmentResponse.model_validate(
            assignment
        )

    def delete(
        self,
        assignment_id,
    ) -> dict:

        assignment = (
            self.assignment_repository.get_by_id(
                assignment_id
            )
        )

        if assignment is None:
            raise ResourceNotFoundError(
                "Priest assignment not found."
            )

        self.assignment_repository.delete(
            assignment
        )

        return {
            "message": "Priest assignment deleted successfully."
        }