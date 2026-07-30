from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.kundli import Kundli
from app.repositories import KundliRepository
from app.schemas import (
    CreateKundliRequest,
    ManageKundliRequest,
    UpdateKundliRequest,
)


class KundliService:
    """
    Business logic for Kundli and astrology requests.
    """

    ALLOWED_SERVICE_TYPES = {
        "KUNDLI",
        "HOROSCOPE",
        "MATCHMAKING",
        "ASTROLOGY_CONSULTATION",
    }

    ALLOWED_STATUSES = {
        "PENDING",
        "ASSIGNED",
        "IN_PROGRESS",
        "COMPLETED",
        "CANCELLED",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = KundliRepository(db)

    def get_all(self) -> list[Kundli]:
        return self.repository.get_all()

    def get_by_id(
        self,
        kundli_id: str,
    ) -> Kundli:
        kundli_uuid = self._parse_uuid(
            kundli_id,
            "Kundli request not found.",
        )

        kundli = self.repository.get_by_id(
            kundli_uuid
        )

        if not kundli:
            raise ResourceNotFoundError(
                "Kundli request not found."
            )

        return kundli

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[Kundli]:
        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        return self.repository.get_by_user_id(
            user_uuid
        )

    def get_by_priest_id(
        self,
        priest_id: str,
    ) -> list[Kundli]:
        priest_uuid = self._parse_uuid(
            priest_id,
            "Invalid priest ID.",
        )

        return self.repository.get_by_priest_id(
            priest_uuid
        )

    def get_by_status(
        self,
        request_status: str,
    ) -> list[Kundli]:
        normalized_status = request_status.upper()

        self._validate_status(
            normalized_status
        )

        return self.repository.get_by_status(
            normalized_status
        )

    def create(
        self,
        user_id: str,
        request: CreateKundliRequest,
    ) -> Kundli:
        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        service_type = request.service_type.upper()

        self._validate_service_type(
            service_type
        )

        kundli = Kundli(
            user_id=user_uuid,
            full_name=request.full_name,
            date_of_birth=request.date_of_birth,
            time_of_birth=request.time_of_birth,
            place_of_birth=request.place_of_birth,
            gender=request.gender,
            service_type=service_type,
            request_status="PENDING",
            user_question=request.user_question,
        )

        return self.repository.create(
            kundli
        )

    def update_owned(
        self,
        kundli_id: str,
        user_id: str,
        request: UpdateKundliRequest,
    ) -> Kundli:
        kundli = self.get_by_id(
            kundli_id
        )

        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        if kundli.user_id != user_uuid:
            raise ResourceNotFoundError(
                "Kundli request not found."
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

        for field, value in update_data.items():
            setattr(
                kundli,
                field,
                value,
            )

        return self.repository.update(
            kundli
        )

    def manage(
        self,
        kundli_id: str,
        request: ManageKundliRequest,
    ) -> Kundli:
        kundli = self.get_by_id(
            kundli_id
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if (
            "request_status" in update_data
            and update_data["request_status"] is not None
        ):
            request_status = update_data[
                "request_status"
            ].upper()

            self._validate_status(
                request_status
            )

            update_data[
                "request_status"
            ] = request_status

        for field, value in update_data.items():
            setattr(
                kundli,
                field,
                value,
            )

        return self.repository.update(
            kundli
        )

    def delete_owned(
        self,
        kundli_id: str,
        user_id: str,
    ) -> None:
        kundli = self.get_by_id(
            kundli_id
        )

        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        if kundli.user_id != user_uuid:
            raise ResourceNotFoundError(
                "Kundli request not found."
            )

        self.repository.delete(
            kundli
        )

    def delete(
        self,
        kundli_id: str,
    ) -> None:
        kundli = self.get_by_id(
            kundli_id
        )

        self.repository.delete(
            kundli
        )

    def _validate_service_type(
        self,
        service_type: str,
    ) -> None:
        if service_type not in self.ALLOWED_SERVICE_TYPES:
            raise ValueError(
                "Invalid Kundli service type."
            )

    def _validate_status(
        self,
        request_status: str,
    ) -> None:
        if request_status not in self.ALLOWED_STATUSES:
            raise ValueError(
                "Invalid Kundli request status."
            )

    @staticmethod
    def _parse_uuid(
        value: str,
        error_message: str,
    ) -> UUID:
        try:
            return UUID(value)

        except (ValueError, TypeError) as exc:
            raise ResourceNotFoundError(
                error_message
            ) from exc