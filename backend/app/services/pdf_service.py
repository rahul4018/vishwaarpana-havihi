from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.db.models.invoice import Invoice
from app.db.models.payment import Payment


class PDFService:
    """
    Service for generating invoice and payment receipt PDF documents.
    """

    @staticmethod
    def _create_document(buffer: BytesIO) -> SimpleDocTemplate:
        """
        Create a standard A4 PDF document.
        """
        return SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

    @staticmethod
    def _create_info_table(data: list[list[str]]) -> Table:
        """
        Create a standard information table.
        """
        table = Table(
            data,
            colWidths=[
                50 * mm,
                110 * mm,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        return table

    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> BytesIO:
        """
        Generate an invoice PDF and return it as an in-memory buffer.
        """

        buffer = BytesIO()
        document = PDFService._create_document(buffer)

        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph(
                "Vishwaarpana Havihi",
                styles["Title"],
            )
        )

        elements.append(
            Paragraph(
                "Invoice",
                styles["Heading2"],
            )
        )

        elements.append(Spacer(1, 10 * mm))

        invoice_data = [
            [
                "Invoice Number",
                str(invoice.invoice_number),
            ],
            [
                "Booking ID",
                str(invoice.booking_id),
            ],
            [
                "Payment ID",
                (
                    str(invoice.payment_id)
                    if invoice.payment_id
                    else "N/A"
                ),
            ],
            [
                "Invoice Status",
                str(invoice.invoice_status),
            ],
            [
                "Issued At",
                (
                    invoice.issued_at.strftime(
                        "%d-%m-%Y %H:%M"
                    )
                    if invoice.issued_at
                    else "N/A"
                ),
            ],
        ]

        elements.append(
            PDFService._create_info_table(
                invoice_data
            )
        )

        elements.append(Spacer(1, 10 * mm))

        amount_data = [
            [
                "Description",
                "Amount",
            ],
            [
                "Subtotal",
                f"INR {invoice.subtotal:.2f}",
            ],
            [
                "Tax",
                f"INR {invoice.tax_amount:.2f}",
            ],
            [
                "Discount",
                f"INR {invoice.discount_amount:.2f}",
            ],
            [
                "Total Amount",
                f"INR {invoice.total_amount:.2f}",
            ],
        ]

        amount_table = Table(
            amount_data,
            colWidths=[
                110 * mm,
                50 * mm,
            ],
        )

        amount_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (1, -1),
                        "RIGHT",
                    ),
                    (
                        "FONTNAME",
                        (0, -1),
                        (-1, -1),
                        "Helvetica-Bold",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        elements.append(amount_table)

        if invoice.notes:
            elements.append(Spacer(1, 10 * mm))

            elements.append(
                Paragraph(
                    "<b>Notes:</b>",
                    styles["Normal"],
                )
            )

            elements.append(Spacer(1, 2 * mm))

            elements.append(
                Paragraph(
                    str(invoice.notes),
                    styles["Normal"],
                )
            )

        elements.append(Spacer(1, 15 * mm))

        elements.append(
            Paragraph(
                "Thank you for using Vishwaarpana Havihi.",
                styles["Normal"],
            )
        )

        document.build(elements)

        buffer.seek(0)

        return buffer

    @staticmethod
    def generate_receipt_pdf(payment: Payment) -> BytesIO:
        """
        Generate a payment receipt PDF and return it as an in-memory buffer.
        """

        buffer = BytesIO()
        document = PDFService._create_document(buffer)

        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph(
                "Vishwaarpana Havihi",
                styles["Title"],
            )
        )

        elements.append(
            Paragraph(
                "Payment Receipt",
                styles["Heading2"],
            )
        )

        elements.append(Spacer(1, 10 * mm))

        receipt_data = [
            [
                "Payment ID",
                str(payment.id),
            ],
            [
                "Booking ID",
                str(payment.booking_id),
            ],
            [
                "Transaction ID",
                (
                    str(payment.transaction_id)
                    if payment.transaction_id
                    else "N/A"
                ),
            ],
            [
                "Payment Status",
                str(payment.payment_status),
            ],
            [
                "Payment Method",
                (
                    str(payment.payment_method)
                    if payment.payment_method
                    else "N/A"
                ),
            ],
            [
                "Gateway",
                (
                    str(payment.gateway)
                    if payment.gateway
                    else "N/A"
                ),
            ],
            [
                "Gateway Payment ID",
                (
                    str(payment.gateway_payment_id)
                    if payment.gateway_payment_id
                    else "N/A"
                ),
            ],
            [
                "Amount Paid",
                f"INR {payment.amount:.2f}",
            ],
            [
                "Paid At",
                (
                    payment.paid_at.strftime(
                        "%d-%m-%Y %H:%M"
                    )
                    if payment.paid_at
                    else "N/A"
                ),
            ],
        ]

        elements.append(
            PDFService._create_info_table(
                receipt_data
            )
        )

        if payment.failure_reason:
            elements.append(Spacer(1, 10 * mm))

            elements.append(
                Paragraph(
                    "<b>Failure Reason:</b>",
                    styles["Normal"],
                )
            )

            elements.append(Spacer(1, 2 * mm))

            elements.append(
                Paragraph(
                    str(payment.failure_reason),
                    styles["Normal"],
                )
            )

        elements.append(Spacer(1, 15 * mm))

        elements.append(
            Paragraph(
                "This receipt is generated for your payment transaction.",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 5 * mm))

        elements.append(
            Paragraph(
                "Thank you for using Vishwaarpana Havihi.",
                styles["Normal"],
            )
        )

        document.build(elements)

        buffer.seek(0)

        return buffer