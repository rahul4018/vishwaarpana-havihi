from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.invoice import Invoice
from app.repositories import (
    BookingRepository,
    InvoiceRepository,
    PaymentRepository,
)
from app.schemas import (
    CreateInvoiceRequest,
    InvoiceResponse,
    UpdateInvoiceRequest,
)


class InvoiceService:
    """
    Invoice business logic.
    """

    def __init__(self, db: Session) -> None:
        self.invoice_repository = InvoiceRepository(db)
        self.booking_repository = BookingRepository(db)
        self.payment_repository = PaymentRepository(db)

    def _generate_invoice_number(self) -> str:
        """
        Generate invoice number such as:
        VH-INV-20260717-000001
        """
        today = date.today().strftime("%Y%m%d")
        count = self.invoice_repository.count() + 1

        return f"VH-INV-{today}-{count:06d}"

    @staticmethod
    def _calculate_total(
        subtotal: Decimal,
        tax_amount: Decimal,
        discount_amount: Decimal,
    ) -> Decimal:
        total = subtotal + tax_amount - discount_amount

        if total < Decimal("0.00"):
            return Decimal("0.00")

        return total

    def create(
        self,
        request: CreateInvoiceRequest,
    ) -> InvoiceResponse:

        booking = self.booking_repository.get_by_id(
            str(request.booking_id)
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        if request.payment_id is not None:
            payment = self.payment_repository.get_by_id(
                str(request.payment_id)
            )

            if payment is None:
                raise ResourceNotFoundError(
                    "Payment not found."
                )

            if payment.booking_id != request.booking_id:
                raise ValueError(
                    "Payment does not belong to this booking."
                )

        total_amount = self._calculate_total(
            request.subtotal,
            request.tax_amount,
            request.discount_amount,
        )

        invoice = Invoice(
            invoice_number=self._generate_invoice_number(),
            booking_id=request.booking_id,
            payment_id=request.payment_id,
            subtotal=request.subtotal,
            tax_amount=request.tax_amount,
            discount_amount=request.discount_amount,
            total_amount=total_amount,
            invoice_status="ISSUED",
            notes=request.notes,
        )

        created = self.invoice_repository.create(
            invoice
        )

        return InvoiceResponse.model_validate(created)

    def get_all(self) -> list[InvoiceResponse]:

        invoices = self.invoice_repository.get_all()

        return [
            InvoiceResponse.model_validate(invoice)
            for invoice in invoices
        ]

    def get_by_id(
        self,
        invoice_id: str,
    ) -> InvoiceResponse:

        invoice = self.invoice_repository.get_by_id(
            invoice_id
        )

        if invoice is None:
            raise ResourceNotFoundError(
                "Invoice not found."
            )

        return InvoiceResponse.model_validate(invoice)

    # ---------------- NEW METHOD ---------------- #

    def get_by_invoice_number(
        self,
        invoice_number: str,
    ) -> Invoice:

        invoice = (
            self.invoice_repository.get_by_invoice_number(
                invoice_number
            )
        )

        if invoice is None:
            raise ResourceNotFoundError(
                "Invoice not found."
            )

        return invoice

    # -------------------------------------------- #

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> list[InvoiceResponse]:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        invoices = self.invoice_repository.get_by_booking_id(
            booking_id
        )

        return [
            InvoiceResponse.model_validate(invoice)
            for invoice in invoices
        ]

    def update(
        self,
        invoice_id: str,
        request: UpdateInvoiceRequest,
    ) -> InvoiceResponse:

        invoice = self.invoice_repository.get_by_id(
            invoice_id
        )

        if invoice is None:
            raise ResourceNotFoundError(
                "Invoice not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "payment_id" in update_data:
            payment_id = update_data["payment_id"]

            if payment_id is not None:
                payment = self.payment_repository.get_by_id(
                    str(payment_id)
                )

                if payment is None:
                    raise ResourceNotFoundError(
                        "Payment not found."
                    )

                if payment.booking_id != invoice.booking_id:
                    raise ValueError(
                        "Payment does not belong to this booking."
                    )

        for field, value in update_data.items():
            setattr(invoice, field, value)

        invoice.total_amount = self._calculate_total(
            invoice.subtotal,
            invoice.tax_amount,
            invoice.discount_amount,
        )

        updated = self.invoice_repository.update(invoice)

        return InvoiceResponse.model_validate(updated)

    def delete(
        self,
        invoice_id: str,
    ) -> None:

        invoice = self.invoice_repository.get_by_id(
            invoice_id
        )

        if invoice is None:
            raise ResourceNotFoundError(
                "Invoice not found."
            )

        self.invoice_repository.delete(invoice)