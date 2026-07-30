from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.enums.quotation_status import QuotationStatus
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.booking_quotation import BookingQuotation
from app.repositories.booking_quotation_repository import (
    BookingQuotationRepository,
)
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking_quotation import (
    BookingQuotationResponse,
    CreateBookingQuotationRequest,
    UpdateBookingQuotationRequest,
)


class BookingQuotationService:
    """
    Booking quotation business logic.
    """

    def __init__(self, db: Session) -> None:
        self.booking_repository = BookingRepository(db)
        self.quotation_repository = (
            BookingQuotationRepository(db)
        )

    def _generate_quotation_number(self) -> str:
        """
        Generate quotation number.
        """

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d%H%M%S"
        )

        return f"QTN-{timestamp}"

    @staticmethod
    def _calculate_total(
        request: CreateBookingQuotationRequest,
    ) -> Decimal:
        return (
            request.priest_cost
            + request.material_cost
            + request.catering_cost
            + request.transport_cost
            + request.miscellaneous_cost
            + request.tax
            - request.discount
        )

    def create(
        self,
        request: CreateBookingQuotationRequest,
    ) -> BookingQuotationResponse:
        """
        Create quotation.
        """

        booking = self.booking_repository.get_by_id(
            str(request.booking_id)
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        existing = (
            self.quotation_repository.get_by_booking_id(
                str(request.booking_id)
            )
        )

        if existing is not None:
            raise ValueError(
                "Quotation already exists for this booking."
            )

        total = self._calculate_total(request)

        quotation = BookingQuotation(
            booking_id=request.booking_id,
            quotation_number=self._generate_quotation_number(),
            priest_cost=request.priest_cost,
            material_cost=request.material_cost,
            catering_cost=request.catering_cost,
            transport_cost=request.transport_cost,
            miscellaneous_cost=request.miscellaneous_cost,
            discount=request.discount,
            tax=request.tax,
            total_amount=total,
            advance_amount=request.advance_amount,
            remaining_amount=(
                total - request.advance_amount
            ),
            notes=request.notes,
            quotation_status=QuotationStatus.DRAFT,
            valid_until=request.valid_until,
        )

        created = self.quotation_repository.create(
            quotation
        )

        return BookingQuotationResponse.model_validate(
            created
        )

    def get_all(
        self,
    ) -> list[BookingQuotationResponse]:

        quotations = (
            self.quotation_repository.get_all()
        )

        return [
            BookingQuotationResponse.model_validate(
                quotation
            )
            for quotation in quotations
        ]

    def get_by_id(
        self,
        quotation_id: str,
    ) -> BookingQuotationResponse:

        quotation = (
            self.quotation_repository.get_by_id(
                quotation_id
            )
        )

        if quotation is None:
            raise ResourceNotFoundError(
                "Quotation not found."
            )

        return BookingQuotationResponse.model_validate(
            quotation
        )

    def get_by_booking(
        self,
        booking_id: str,
    ) -> BookingQuotationResponse:

        quotation = (
            self.quotation_repository.get_by_booking_id(
                booking_id
            )
        )

        if quotation is None:
            raise ResourceNotFoundError(
                "Quotation not found."
            )

        return BookingQuotationResponse.model_validate(
            quotation
        )

    def update(
        self,
        quotation_id: str,
        request: UpdateBookingQuotationRequest,
    ) -> BookingQuotationResponse:

        quotation = (
            self.quotation_repository.get_by_id(
                quotation_id
            )
        )

        if quotation is None:
            raise ResourceNotFoundError(
                "Quotation not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                quotation,
                field,
                value,
            )

        quotation.total_amount = (
            quotation.priest_cost
            + quotation.material_cost
            + quotation.catering_cost
            + quotation.transport_cost
            + quotation.miscellaneous_cost
            + quotation.tax
            - quotation.discount
        )

        quotation.remaining_amount = (
            quotation.total_amount
            - quotation.advance_amount
        )

        updated = self.quotation_repository.update(
            quotation
        )

        return BookingQuotationResponse.model_validate(
            updated
        )

    def delete(
        self,
        quotation_id: str,
    ) -> None:

        quotation = (
            self.quotation_repository.get_by_id(
                quotation_id
            )
        )

        if quotation is None:
            raise ResourceNotFoundError(
                "Quotation not found."
            )

        self.quotation_repository.delete(
            quotation
        )