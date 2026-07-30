from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.repositories.booking_repository import BookingRepository
from app.services.workflow.booking_workflow_service import (
    BookingWorkflowService,
)

router = APIRouter(
    prefix="/booking-workflow",
    tags=["Booking Workflow"],
)


@router.patch(
    "/{booking_id}/review",
    summary="Move booking to review",
)
def review_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    repository = BookingRepository(db)

    booking = repository.get_by_id(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    workflow = BookingWorkflowService(db)

    try:
        workflow.review_booking(
            booking=booking,
            updated_by=str(current_user.id),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "success": True,
        "message": "Booking moved to review.",
        "booking_status": booking.booking_status,
    }


@router.patch(
    "/{booking_id}/prepare-quotation",
    summary="Prepare quotation",
)
def prepare_quotation(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    repository = BookingRepository(db)

    booking = repository.get_by_id(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found.",
        )

    workflow = BookingWorkflowService(db)

    try:
        workflow.prepare_quotation(
            booking,
            str(current_user.id),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "success": True,
        "message": "Quotation preparation started.",
        "booking_status": booking.booking_status,
    }


@router.patch(
    "/{booking_id}/send-quotation",
    summary="Send quotation",
)
def send_quotation(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    repository = BookingRepository(db)

    booking = repository.get_by_id(booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found.",
        )

    workflow = BookingWorkflowService(db)

    try:
        workflow.send_quotation(
            booking,
            str(current_user.id),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "success": True,
        "message": "Quotation sent successfully.",
        "booking_status": booking.booking_status,
    }