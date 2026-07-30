from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateInvoiceRequest,
    InvoiceResponse,
    UpdateInvoiceRequest,
)
from app.services import InvoiceService
from app.services.pdf_service import PDFService


router = APIRouter(
    prefix="/invoices",
    tags=["Invoice"],
)


@router.get(
    "",
    response_model=list[InvoiceResponse],
    summary="Get all invoices",
)
def get_all_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = InvoiceService(db)
    return service.get_all()


@router.get(
    "/booking/{booking_id}",
    response_model=list[InvoiceResponse],
    summary="Get invoices by booking ID",
)
def get_invoices_by_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InvoiceService(db)

    try:
        return service.get_by_booking_id(booking_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{invoice_number}/download",
    summary="Download invoice PDF",
    response_class=StreamingResponse,
)
def download_invoice_pdf(
    invoice_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and download an invoice as a PDF document by its invoice number.
    """
    service = InvoiceService(db)

    try:
        invoice = service.get_by_invoice_number(invoice_number)
    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    pdf_buffer = PDFService.generate_invoice_pdf(invoice)
    filename = f"invoice_{invoice.invoice_number}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Get invoice by ID",
)
def get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InvoiceService(db)

    try:
        return service.get_by_id(invoice_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create invoice",
)
def create_invoice(
    request: CreateInvoiceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = InvoiceService(db)

    try:
        return service.create(request)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Update invoice",
)
def update_invoice(
    invoice_id: str,
    request: UpdateInvoiceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = InvoiceService(db)

    try:
        return service.update(
            invoice_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete invoice",
)
def delete_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    service = InvoiceService(db)

    try:
        service.delete(invoice_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc