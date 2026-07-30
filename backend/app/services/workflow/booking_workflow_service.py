from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.enums.booking_status import BookingStatus
from app.db.models.booking import Booking
from app.db.models.booking_status_history import BookingStatusHistory


class BookingWorkflowService:
    """
    Handles booking workflow state transitions.
    """

    ALLOWED_TRANSITIONS = {
        BookingStatus.REQUESTED: {
            BookingStatus.REVIEWING,
            BookingStatus.CANCELLED,
        },
        BookingStatus.REVIEWING: {
            BookingStatus.QUOTATION_PREPARING,
            BookingStatus.CANCELLED,
        },
        BookingStatus.QUOTATION_PREPARING: {
            BookingStatus.QUOTATION_SENT,
        },
        BookingStatus.QUOTATION_SENT: {
            BookingStatus.QUOTATION_ACCEPTED,
            BookingStatus.CANCELLED,
        },
        BookingStatus.QUOTATION_ACCEPTED: {
            BookingStatus.ADVANCE_PAYMENT_PENDING,
        },
        BookingStatus.ADVANCE_PAYMENT_PENDING: {
            BookingStatus.ADVANCE_PAID,
        },
        BookingStatus.ADVANCE_PAID: {
            BookingStatus.PAYMENT_VERIFIED,
        },
        BookingStatus.PAYMENT_VERIFIED: {
            BookingStatus.PRIEST_ASSIGNED,
        },
        BookingStatus.PRIEST_ASSIGNED: {
            BookingStatus.MATERIALS_READY,
        },
        BookingStatus.MATERIALS_READY: {
            BookingStatus.CALENDAR_SHARED,
        },
        BookingStatus.CALENDAR_SHARED: {
            BookingStatus.SERVICE_IN_PROGRESS,
        },
        BookingStatus.SERVICE_IN_PROGRESS: {
            BookingStatus.SERVICE_COMPLETED,
        },
        BookingStatus.SERVICE_COMPLETED: {
            BookingStatus.FINAL_PAYMENT_PENDING,
        },
        BookingStatus.FINAL_PAYMENT_PENDING: {
            BookingStatus.COMPLETED,
        },
        BookingStatus.COMPLETED: set(),
        BookingStatus.CANCELLED: set(),
    }

    def __init__(self, db: Session):
        self.db = db

    def change_status(
        self,
        booking: Booking,
        status: BookingStatus,
        updated_by: str,
        remarks: str | None = None,
    ) -> Booking:

        current_status = booking.booking_status

        allowed = self.ALLOWED_TRANSITIONS.get(
            current_status,
            set(),
        )

        if status not in allowed:
            raise ValueError(
                f"Invalid workflow transition "
                f"{current_status.value} -> {status.value}"
            )

        booking.booking_status = status

        history = BookingStatusHistory(
            booking_id=booking.id,
            status=status,
            updated_by=updated_by,
            remarks=remarks,
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(booking)

        return booking

    def review_booking(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.REVIEWING,
            updated_by,
            "Booking moved for review.",
        )

    def prepare_quotation(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.QUOTATION_PREPARING,
            updated_by,
            "Preparing quotation.",
        )

    def send_quotation(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.QUOTATION_SENT,
            updated_by,
            "Quotation sent to customer.",
        )

    def accept_quotation(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.QUOTATION_ACCEPTED,
            updated_by,
            "Quotation accepted.",
        )

    def request_advance_payment(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.ADVANCE_PAYMENT_PENDING,
            updated_by,
            "Advance payment requested.",
        )

    def verify_advance_payment(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.ADVANCE_PAID,
            updated_by,
            "Advance payment verified.",
        )

    def verify_payment(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.PAYMENT_VERIFIED,
            updated_by,
            "Payment verified.",
        )

    def assign_priest(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.PRIEST_ASSIGNED,
            updated_by,
            "Priest assigned.",
        )

    def prepare_materials(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.MATERIALS_READY,
            updated_by,
            "Materials ready.",
        )

    def share_calendar(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.CALENDAR_SHARED,
            updated_by,
            "Calendar shared.",
        )

    def start_service(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.SERVICE_IN_PROGRESS,
            updated_by,
            "Service started.",
        )

    def complete_service(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.SERVICE_COMPLETED,
            updated_by,
            "Service completed.",
        )

    def request_final_payment(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.FINAL_PAYMENT_PENDING,
            updated_by,
            "Final payment pending.",
        )

    def complete_booking(
        self,
        booking: Booking,
        updated_by: str,
    ) -> Booking:
        return self.change_status(
            booking,
            BookingStatus.COMPLETED,
            updated_by,
            "Booking completed.",
        )

    def cancel_booking(
        self,
        booking: Booking,
        updated_by: str,
        remarks: str | None = None,
    ) -> Booking:
        booking.booking_status = BookingStatus.CANCELLED

        history = BookingStatusHistory(
            booking_id=booking.id,
            status=BookingStatus.CANCELLED,
            updated_by=updated_by,
            remarks=remarks or "Booking cancelled.",
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(booking)

        return booking