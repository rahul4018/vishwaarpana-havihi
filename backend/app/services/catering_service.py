from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.catering import Catering
from app.repositories import CateringRepository
from app.schemas import (
    CreateCateringRequest,
    UpdateCateringRequest,
)


class CateringService:
    """
    Business logic for catering and prasadam services.
    """

    ALLOWED_SERVICE_TYPES = {
        "CATERING",
        "PRASADAM",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = CateringRepository(db)

    def get_all(self) -> list[Catering]:
        return self.repository.get_all()

    def get_available(self) -> list[Catering]:
        return self.repository.get_available()

    def get_by_id(
        self,
        catering_id: str,
    ) -> Catering:
        try:
            catering_uuid = UUID(catering_id)
        except ValueError as exc:
            raise ResourceNotFoundError(
                "Catering service not found."
            ) from exc

        catering = self.repository.get_by_id(
            catering_uuid
        )

        if not catering:
            raise ResourceNotFoundError(
                "Catering service not found."
            )

        return catering

    def get_by_temple_id(
        self,
        temple_id: str,
    ) -> list[Catering]:
        try:
            temple_uuid = UUID(temple_id)
        except ValueError as exc:
            raise ResourceNotFoundError(
                "Invalid temple ID."
            ) from exc

        return self.repository.get_by_temple_id(
            temple_uuid
        )

    def get_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[Catering]:
        try:
            pooja_uuid = UUID(pooja_id)
        except ValueError as exc:
            raise ResourceNotFoundError(
                "Invalid pooja ID."
            ) from exc

        return self.repository.get_by_pooja_id(
            pooja_uuid
        )

    def get_by_service_type(
        self,
        service_type: str,
    ) -> list[Catering]:
        normalized_type = service_type.upper()

        if normalized_type not in self.ALLOWED_SERVICE_TYPES:
            raise ValueError(
                "Service type must be CATERING or PRASADAM."
            )

        return self.repository.get_by_service_type(
            normalized_type
        )

    def create(
        self,
        request: CreateCateringRequest,
    ) -> Catering:
        service_type = request.service_type.upper()

        self._validate_service_type(
            service_type
        )

        self._validate_people_range(
            request.minimum_people,
            request.maximum_people,
        )

        catering = Catering(
            temple_id=request.temple_id,
            pooja_id=request.pooja_id,
            name=request.name,
            service_type=service_type,
            description=request.description,
            menu_details=request.menu_details,
            price_per_person=request.price_per_person,
            minimum_people=request.minimum_people,
            maximum_people=request.maximum_people,
            is_vegetarian=request.is_vegetarian,
            is_available=request.is_available,
            image_url=request.image_url,
        )

        return self.repository.create(
            catering
        )

    def update(
        self,
        catering_id: str,
        request: UpdateCateringRequest,
    ) -> Catering:
        catering = self.get_by_id(
            catering_id
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "service_type" in update_data:
            service_type = update_data[
                "service_type"
            ].upper()

            self._validate_service_type(
                service_type
            )

            update_data[
                "service_type"
            ] = service_type

        minimum_people = update_data.get(
            "minimum_people",
            catering.minimum_people,
        )

        maximum_people = update_data.get(
            "maximum_people",
            catering.maximum_people,
        )

        self._validate_people_range(
            minimum_people,
            maximum_people,
        )

        for field, value in update_data.items():
            setattr(
                catering,
                field,
                value,
            )

        return self.repository.update(
            catering
        )

    def delete(
        self,
        catering_id: str,
    ) -> None:
        catering = self.get_by_id(
            catering_id
        )

        self.repository.delete(
            catering
        )

    def _validate_service_type(
        self,
        service_type: str,
    ) -> None:
        if service_type not in self.ALLOWED_SERVICE_TYPES:
            raise ValueError(
                "Service type must be CATERING or PRASADAM."
            )

    @staticmethod
    def _validate_people_range(
        minimum_people: int,
        maximum_people: int | None,
    ) -> None:
        if (
            maximum_people is not None
            and maximum_people < minimum_people
        ):
            raise ValueError(
                "Maximum people cannot be less than minimum people."
            )