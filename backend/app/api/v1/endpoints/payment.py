from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.repositories import PaymentRepository
from app.schemas import (
    CreatePaymentRequest,
    PaymentResponse,
    UpdatePaymentRequest,
)
from app.services import PaymentService
from app.services.pdf_service import PDFService


router = APIRouter(
    prefix="/payments",
    tags=["Payment"],
)


@router.get(
    "",
    response_model=list[PaymentResponse],
    summary="Get all payments",
)
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all payment records.
    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = PaymentService(db)

    return service.get_all()


@router.get(
    "/booking/{booking_id}",
    response_model=list[PaymentResponse],
    summary="Get payments by booking ID",
)
def get_payments_by_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all payment records associated with a booking.
    """

    service = PaymentService(db)

    try:
        return service.get_by_booking_id(
            booking_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{payment_id}/receipt",
    summary="Download payment receipt PDF",
    response_class=StreamingResponse,
)
def download_payment_receipt(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download a payment receipt as a PDF document.
    """

    repository = PaymentRepository(db)

    payment = repository.get_by_id(
        payment_id
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    pdf_buffer = PDFService.generate_receipt_pdf(
        payment
    )

    filename = (
        f"receipt_{payment.id}.pdf"
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Get payment by ID",
)
def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a payment record by ID.
    """

    service = PaymentService(db)

    try:
        return service.get_by_id(
            payment_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create payment",
)
def create_payment(
    request: CreatePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a payment record for a booking.
    """

    service = PaymentService(db)

    try:
        return service.create(
            request
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Update payment",
)
def update_payment(
    payment_id: str,
    request: UpdatePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Update payment information or payment status.
    """

    service = PaymentService(db)

    try:
        return service.update(
            payment_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete payment",
)
def delete_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Delete a payment record.
    Accessible only to SUPER_ADMIN.
    """

    service = PaymentService(db)

    try:
        service.delete(
            payment_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc