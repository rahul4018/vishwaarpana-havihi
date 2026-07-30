from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    ResourceNotFoundError,
)
from app.db.models.pooja import Pooja
from app.repositories import PoojaRepository
from app.schemas import (
    CreatePoojaRequest,
    PoojaResponse,
    UpdatePoojaRequest,
)


class PoojaService:
    """
    Pooja business logic.
    """

    def __init__(self, db: Session) -> None:
        self.pooja_repository = PoojaRepository(db)

    def create(
        self,
        request: CreatePoojaRequest,
    ) -> PoojaResponse:

        pooja = Pooja(
            temple_id=request.temple_id,
            category_id=request.category_id,
            priest_id=request.priest_id,
            name=request.name,
            slug=request.slug,
            description=request.description,
            duration_minutes=request.duration_minutes,
            price=request.price,
            max_participants=request.max_participants,
            online_booking=request.online_booking,
            is_active=True,
        )

        created = self.pooja_repository.create(pooja)

        return PoojaResponse.model_validate(created)

    def get_by_id(
        self,
        pooja_id: str,
    ) -> PoojaResponse:

        pooja = self.pooja_repository.get_by_id(
            pooja_id,
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        return PoojaResponse.model_validate(pooja)

    def get_all(
        self,
    ) -> list[PoojaResponse]:

        poojas = self.pooja_repository.get_all()

        return [
            PoojaResponse.model_validate(
                pooja,
            )
            for pooja in poojas
        ]

    def update(
        self,
        pooja_id: str,
        request: UpdatePoojaRequest,
    ) -> PoojaResponse:

        pooja = self.pooja_repository.get_by_id(
            pooja_id,
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                pooja,
                field,
                value,
            )

        updated = self.pooja_repository.update(
            pooja,
        )

        return PoojaResponse.model_validate(
            updated,
        )

    def delete(
        self,
        pooja_id: str,
    ) -> None:

        pooja = self.pooja_repository.get_by_id(
            pooja_id,
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        self.pooja_repository.delete(
            pooja,
        )