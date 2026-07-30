from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    BookingResponse,
    CreateBookingRequest,
    UpdateBookingRequest,
)
from app.services import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"],
)


@router.get(
    "",
    response_model=list[BookingResponse],
    summary="Get all bookings",
)
def get_all_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)
    return service.get_all()


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Get booking by ID",
)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    try:
        return service.get_by_id(booking_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create booking",
)
def create_booking(
    request: CreateBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.create(
        request,
        current_user.id,
    )


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Update booking",
)
def update_booking(
    booking_id: str,
    request: UpdateBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = BookingService(db)

    try:
        return service.update(
            booking_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete booking",
)
def delete_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    service = BookingService(db)

    try:
        service.delete(booking_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc