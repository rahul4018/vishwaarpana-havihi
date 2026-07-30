from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.consultation import Consultation
from app.repositories import ConsultationRepository
from app.schemas import (
    CreateConsultationRequest,
    ManageConsultationRequest,
    UpdateConsultationRequest,
)


class ConsultationService:
    """
    Business logic for audio and video consultations.
    """

    ALLOWED_TYPES = {
        "AUDIO",
        "VIDEO",
    }

    ALLOWED_STATUSES = {
        "PENDING",
        "CONFIRMED",
        "SCHEDULED",
        "IN_PROGRESS",
        "COMPLETED",
        "CANCELLED",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = ConsultationRepository(db)

    def get_all(self) -> list[Consultation]:
        return self.repository.get_all()

    def get_by_id(
        self,
        consultation_id: str,
    ) -> Consultation:
        consultation_uuid = self._parse_uuid(
            consultation_id,
            "Consultation not found.",
        )

        consultation = self.repository.get_by_id(
            consultation_uuid
        )

        if not consultation:
            raise ResourceNotFoundError(
                "Consultation not found."
            )

        return consultation

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[Consultation]:
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
    ) -> list[Consultation]:
        priest_uuid = self._parse_uuid(
            priest_id,
            "Invalid priest ID.",
        )

        return self.repository.get_by_priest_id(
            priest_uuid
        )

    def get_by_kundli_id(
        self,
        kundli_id: str,
    ) -> list[Consultation]:
        kundli_uuid = self._parse_uuid(
            kundli_id,
            "Invalid Kundli ID.",
        )

        return self.repository.get_by_kundli_id(
            kundli_uuid
        )

    def get_by_status(
        self,
        consultation_status: str,
    ) -> list[Consultation]:
        normalized_status = (
            consultation_status.upper()
        )

        self._validate_status(
            normalized_status
        )

        return self.repository.get_by_status(
            normalized_status
        )

    def get_by_type(
        self,
        consultation_type: str,
    ) -> list[Consultation]:
        normalized_type = (
            consultation_type.upper()
        )

        self._validate_type(
            normalized_type
        )

        return self.repository.get_by_type(
            normalized_type
        )

    def create(
        self,
        user_id: str,
        request: CreateConsultationRequest,
    ) -> Consultation:
        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        consultation_type = (
            request.consultation_type.upper()
        )

        self._validate_type(
            consultation_type
        )

        consultation = Consultation(
            user_id=user_uuid,
            priest_id=request.priest_id,
            kundli_id=request.kundli_id,
            consultation_type=consultation_type,
            consultation_status="PENDING",
            scheduled_at=request.scheduled_at,
            duration_minutes=request.duration_minutes,
            topic=request.topic,
            user_question=request.user_question,
        )

        return self.repository.create(
            consultation
        )

    def update_owned(
        self,
        consultation_id: str,
        user_id: str,
        request: UpdateConsultationRequest,
    ) -> Consultation:
        consultation = self.get_by_id(
            consultation_id
        )

        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        if consultation.user_id != user_uuid:
            raise ResourceNotFoundError(
                "Consultation not found."
            )

        if consultation.consultation_status in {
            "IN_PROGRESS",
            "COMPLETED",
            "CANCELLED",
        }:
            raise ValueError(
                "This consultation can no longer be updated."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if (
            "consultation_type" in update_data
            and update_data["consultation_type"]
            is not None
        ):
            consultation_type = update_data[
                "consultation_type"
            ].upper()

            self._validate_type(
                consultation_type
            )

            update_data[
                "consultation_type"
            ] = consultation_type

        for field, value in update_data.items():
            setattr(
                consultation,
                field,
                value,
            )

        return self.repository.update(
            consultation
        )

    def manage(
        self,
        consultation_id: str,
        request: ManageConsultationRequest,
    ) -> Consultation:
        consultation = self.get_by_id(
            consultation_id
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if (
            "consultation_status" in update_data
            and update_data[
                "consultation_status"
            ]
            is not None
        ):
            consultation_status = update_data[
                "consultation_status"
            ].upper()

            self._validate_status(
                consultation_status
            )

            update_data[
                "consultation_status"
            ] = consultation_status

        for field, value in update_data.items():
            setattr(
                consultation,
                field,
                value,
            )

        return self.repository.update(
            consultation
        )

    def cancel_owned(
        self,
        consultation_id: str,
        user_id: str,
    ) -> Consultation:
        consultation = self.get_by_id(
            consultation_id
        )

        user_uuid = self._parse_uuid(
            user_id,
            "Invalid user ID.",
        )

        if consultation.user_id != user_uuid:
            raise ResourceNotFoundError(
                "Consultation not found."
            )

        if consultation.consultation_status in {
            "IN_PROGRESS",
            "COMPLETED",
            "CANCELLED",
        }:
            raise ValueError(
                "This consultation cannot be cancelled."
            )

        consultation.consultation_status = (
            "CANCELLED"
        )

        return self.repository.update(
            consultation
        )

    def delete(
        self,
        consultation_id: str,
    ) -> None:
        consultation = self.get_by_id(
            consultation_id
        )

        self.repository.delete(
            consultation
        )

    def _validate_type(
        self,
        consultation_type: str,
    ) -> None:
        if (
            consultation_type
            not in self.ALLOWED_TYPES
        ):
            raise ValueError(
                "Invalid consultation type. "
                "Allowed types are AUDIO and VIDEO."
            )

    def _validate_status(
        self,
        consultation_status: str,
    ) -> None:
        if (
            consultation_status
            not in self.ALLOWED_STATUSES
        ):
            raise ValueError(
                "Invalid consultation status."
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