from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.core.enums.booking_status import BookingStatus
from app.core.exceptions.http_exceptions import (
    ResourceNotFoundError,
)
from app.db.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from app.repositories.pooja_repository import PoojaRepository
from app.repositories.temple_repository import TempleRepository
from app.schemas.booking import (
    BookingResponse,
    CreateBookingRequest,
    UpdateBookingRequest,
)


class BookingService:
    """
    Booking business logic.
    """

    def __init__(self, db: Session) -> None:
        self.booking_repository = BookingRepository(db)
        self.temple_repository = TempleRepository(db)
        self.pooja_repository = PoojaRepository(db)

    def _generate_booking_number(self) -> str:
        bookings = self.booking_repository.get_all()
        return (
            f"VH-{date.today().strftime('%Y%m%d')}-"
            f"{len(bookings)+1:06d}"
        )

    def create(
        self,
        request: CreateBookingRequest,
        user_id: str,
    ) -> BookingResponse:

        temple = self.temple_repository.get_by_id(
            request.temple_id,
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        pooja = self.pooja_repository.get_by_id(
            request.pooja_id,
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        booking = Booking(
            booking_number=self._generate_booking_number(),
            user_id=user_id,
            temple_id=request.temple_id,
            pooja_id=request.pooja_id,
            booking_date=request.booking_date,
            booking_time=request.booking_time,
            participants=request.participants,
            devotee_name=request.devotee_name,
            devotee_mobile=request.devotee_mobile,
            devotee_email=request.devotee_email,
            special_notes=request.special_notes,
            booking_status=BookingStatus.REQUESTED,
            payment_status="PENDING",
        )

        created = self.booking_repository.create(
            booking
        )

        return BookingResponse.model_validate(
            created
        )

    def get_by_id(
        self,
        booking_id: str,
    ) -> BookingResponse:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        return BookingResponse.model_validate(
            booking
        )

    def get_all(
        self,
    ) -> list[BookingResponse]:

        bookings = self.booking_repository.get_all()

        return [
            BookingResponse.model_validate(
                booking
            )
            for booking in bookings
        ]

    def update(
        self,
        booking_id: str,
        request: UpdateBookingRequest,
    ) -> BookingResponse:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        # Workflow status must only be changed
        # through BookingWorkflowService.
        update_data.pop("booking_status", None)

        for field, value in update_data.items():
            setattr(
                booking,
                field,
                value,
            )

        updated = self.booking_repository.update(
            booking
        )

        return BookingResponse.model_validate(
            updated
        )

    def delete(
        self,
        booking_id: str,
    ) -> None:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        self.booking_repository.delete(
            booking
        )