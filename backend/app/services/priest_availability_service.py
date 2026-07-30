from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestError,
    ResourceNotFoundError,
)
from app.db.models.priest_availability import PriestAvailability
from app.repositories.priest_availability_repository import (
    PriestAvailabilityRepository,
)
from app.repositories.priest_repository import PriestRepository
from app.schemas.priest_availability import (
    CreatePriestAvailabilityRequest,
    PriestAvailabilityResponse,
    UpdatePriestAvailabilityRequest,
)


class PriestAvailabilityService:
    """
    Business logic for Priest Availability.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = PriestAvailabilityRepository(db)
        self.priest_repository = PriestRepository(db)

    def create(
        self,
        request: CreatePriestAvailabilityRequest,
    ) -> PriestAvailabilityResponse:

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

        if request.start_time >= request.end_time:
            raise BadRequestError(
                "Start time must be before end time."
            )

        existing = self.repository.get_priest_schedule(
            request.priest_id,
            request.available_date,
        )

        for slot in existing:
            if (
                request.start_time < slot.end_time
                and request.end_time > slot.start_time
            ):
                raise BadRequestError(
                    "Availability overlaps with an existing slot."
                )

        availability = PriestAvailability(
            priest_id=request.priest_id,
            available_date=request.available_date,
            start_time=request.start_time,
            end_time=request.end_time,
            is_available=request.is_available,
            remarks=request.remarks,
        )

        availability = self.repository.create(
            availability
        )

        return PriestAvailabilityResponse.model_validate(
            availability
        )

    def get_all(
        self,
    ) -> list[PriestAvailabilityResponse]:

        records = self.repository.get_all()

        return [
            PriestAvailabilityResponse.model_validate(
                record
            )
            for record in records
        ]

    def get_by_id(
        self,
        availability_id: UUID,
    ) -> PriestAvailabilityResponse:

        availability = self.repository.get_by_id(
            availability_id
        )

        if availability is None:
            raise ResourceNotFoundError(
                "Availability not found."
            )

        return PriestAvailabilityResponse.model_validate(
            availability
        )

    def get_by_priest(
        self,
        priest_id: UUID,
    ) -> list[PriestAvailabilityResponse]:

        records = self.repository.get_by_priest(
            priest_id
        )

        return [
            PriestAvailabilityResponse.model_validate(
                record
            )
            for record in records
        ]

    def get_by_date(
        self,
        available_date: date,
    ) -> list[PriestAvailabilityResponse]:

        records = self.repository.get_by_date(
            available_date
        )

        return [
            PriestAvailabilityResponse.model_validate(
                record
            )
            for record in records
        ]

    def update(
        self,
        availability_id: UUID,
        request: UpdatePriestAvailabilityRequest,
    ) -> PriestAvailabilityResponse:

        availability = self.repository.get_by_id(
            availability_id
        )

        if availability is None:
            raise ResourceNotFoundError(
                "Availability not found."
            )

        if request.available_date is not None:
            availability.available_date = (
                request.available_date
            )

        if request.start_time is not None:
            availability.start_time = (
                request.start_time
            )

        if request.end_time is not None:
            availability.end_time = (
                request.end_time
            )

        if (
            availability.start_time
            >= availability.end_time
        ):
            raise BadRequestError(
                "Start time must be before end time."
            )

        if request.is_available is not None:
            availability.is_available = (
                request.is_available
            )

        if request.remarks is not None:
            availability.remarks = request.remarks

        availability = self.repository.update(
            availability
        )

        return PriestAvailabilityResponse.model_validate(
            availability
        )

    def delete(
        self,
        availability_id: UUID,
    ) -> dict:

        availability = self.repository.get_by_id(
            availability_id
        )

        if availability is None:
            raise ResourceNotFoundError(
                "Availability not found."
            )

        self.repository.delete(
            availability
        )

        return {
            "message": "Priest availability deleted successfully."
        }