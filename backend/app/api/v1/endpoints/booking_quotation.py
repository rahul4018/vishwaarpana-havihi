from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.booking_quotation import (
    BookingQuotationResponse,
    CreateBookingQuotationRequest,
    UpdateBookingQuotationRequest,
)
from app.services.booking_quotation_service import (
    BookingQuotationService,
)

router = APIRouter(
    prefix="/booking-quotations",
    tags=["Booking Quotation"],
)


@router.get(
    "",
    response_model=list[BookingQuotationResponse],
)
def get_all_quotations(
    db: Session = Depends(get_db),
):
    service = BookingQuotationService(db)
    return service.get_all()


@router.get(
    "/{quotation_id}",
    response_model=BookingQuotationResponse,
)
def get_quotation(
    quotation_id: str,
    db: Session = Depends(get_db),
):
    service = BookingQuotationService(db)
    return service.get_by_id(quotation_id)


@router.get(
    "/booking/{booking_id}",
    response_model=BookingQuotationResponse,
)
def get_booking_quotation(
    booking_id: str,
    db: Session = Depends(get_db),
):
    service = BookingQuotationService(db)
    return service.get_by_booking(booking_id)


@router.post(
    "",
    response_model=BookingQuotationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_quotation(
    request: CreateBookingQuotationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "SUPER_ADMIN",
        )
    ),
):
    service = BookingQuotationService(db)
    return service.create(request)


@router.put(
    "/{quotation_id}",
    response_model=BookingQuotationResponse,
)
def update_quotation(
    quotation_id: str,
    request: UpdateBookingQuotationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "SUPER_ADMIN",
        )
    ),
):
    service = BookingQuotationService(db)
    return service.update(
        quotation_id,
        request,
    )


@router.delete(
    "/{quotation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_quotation(
    quotation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "SUPER_ADMIN",
        )
    ),
):
    service = BookingQuotationService(db)
    service.delete(quotation_id)