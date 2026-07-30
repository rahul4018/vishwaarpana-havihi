from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    BadRequestError,
    ResourceNotFoundError,
)
from app.db.models.priest import Priest
from app.repositories import PriestRepository
from app.schemas import (
    CreatePriestRequest,
    PriestResponse,
    UpdatePriestRequest,
)


class PriestService:
    """
    Priest business logic.
    """

    def __init__(self, db: Session) -> None:
        self.priest_repository = PriestRepository(db)

    def create(
        self,
        request: CreatePriestRequest,
    ) -> PriestResponse:

        existing_email = self.priest_repository.get_by_email(
            request.email,
        )

        if existing_email is not None:
            raise BadRequestError(
                "Priest with this email already exists."
            )

        existing_phone = self.priest_repository.get_by_phone(
            request.phone,
        )

        if existing_phone is not None:
            raise BadRequestError(
                "Priest with this phone number already exists."
            )

        priest = Priest(
            temple_id=request.temple_id,
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            experience_years=request.experience_years,
            specialization=request.specialization,
            bio=request.bio,
            is_active=True,
        )

        created = self.priest_repository.create(priest)

        return PriestResponse.model_validate(created)

    def get_by_id(
        self,
        priest_id: str,
    ) -> PriestResponse:

        priest = self.priest_repository.get_by_id(priest_id)

        if priest is None:
            raise ResourceNotFoundError(
                "Priest not found."
            )

        return PriestResponse.model_validate(priest)

    def get_all(self) -> list[PriestResponse]:

        priests = self.priest_repository.get_all()

        return [
            PriestResponse.model_validate(priest)
            for priest in priests
        ]

    def update(
        self,
        priest_id: str,
        request: UpdatePriestRequest,
    ) -> PriestResponse:

        priest = self.priest_repository.get_by_id(priest_id)

        if priest is None:
            raise ResourceNotFoundError(
                "Priest not found."
            )

        if (
            request.email is not None
            and request.email != priest.email
        ):
            existing_email = self.priest_repository.get_by_email(
                request.email,
            )

            if existing_email is not None:
                raise BadRequestError(
                    "Priest with this email already exists."
                )

        if (
            request.phone is not None
            and request.phone != priest.phone
        ):
            existing_phone = self.priest_repository.get_by_phone(
                request.phone,
            )

            if existing_phone is not None:
                raise BadRequestError(
                    "Priest with this phone number already exists."
                )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(priest, field, value)

        updated = self.priest_repository.update(priest)

        return PriestResponse.model_validate(updated)

    def delete(
        self,
        priest_id: str,
    ) -> None:

        priest = self.priest_repository.get_by_id(priest_id)

        if priest is None:
            raise ResourceNotFoundError(
                "Priest not found."
            )

        self.priest_repository.delete(priest)