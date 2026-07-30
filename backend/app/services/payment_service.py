from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.payment import Payment
from app.repositories import (
    BookingRepository,
    PaymentRepository,
)
from app.schemas import (
    CreatePaymentRequest,
    PaymentResponse,
    UpdatePaymentRequest,
)


class PaymentService:
    """
    Payment business logic.
    """

    def __init__(self, db: Session) -> None:
        self.payment_repository = PaymentRepository(db)
        self.booking_repository = BookingRepository(db)

    def create(
        self,
        request: CreatePaymentRequest,
    ) -> PaymentResponse:
        """
        Create a payment record for an existing booking.
        """

        booking = self.booking_repository.get_by_id(
            str(request.booking_id)
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        payment = Payment(
            booking_id=request.booking_id,
            amount=request.amount,
            payment_method=request.payment_method,
            payment_status="PENDING",
            gateway=request.gateway,
        )

        created = self.payment_repository.create(
            payment
        )

        return PaymentResponse.model_validate(
            created
        )

    def get_all(
        self,
    ) -> list[PaymentResponse]:
        """
        Return all payments.
        """

        payments = self.payment_repository.get_all()

        return [
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]

    def get_by_id(
        self,
        payment_id: str,
    ) -> PaymentResponse:
        """
        Return payment by ID.
        """

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ResourceNotFoundError(
                "Payment not found."
            )

        return PaymentResponse.model_validate(
            payment
        )

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> list[PaymentResponse]:
        """
        Return payments associated with a booking.
        """

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        payments = (
            self.payment_repository.get_by_booking_id(
                booking_id
            )
        )

        return [
            PaymentResponse.model_validate(payment)
            for payment in payments
        ]

    def update(
        self,
        payment_id: str,
        request: UpdatePaymentRequest,
    ) -> PaymentResponse:
        """
        Update payment information.
        """

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ResourceNotFoundError(
                "Payment not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                payment,
                field,
                value,
            )

        updated = self.payment_repository.update(
            payment
        )

        return PaymentResponse.model_validate(
            updated
        )

    def delete(
        self,
        payment_id: str,
    ) -> None:
        """
        Delete payment record.
        """

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ResourceNotFoundError(
                "Payment not found."
            )

        self.payment_repository.delete(
            payment
        )