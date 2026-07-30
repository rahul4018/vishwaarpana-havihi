from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    ConsultationResponse,
    CreateConsultationRequest,
    ManageConsultationRequest,
    UpdateConsultationRequest,
)
from app.services import ConsultationService


router = APIRouter(
    prefix="/consultations",
    tags=["Consultation"],
)


# ============================================================
# ADMIN: GET ALL CONSULTATIONS
# ============================================================

@router.get(
    "",
    response_model=list[ConsultationResponse],
    summary="Get all consultations",
)
def get_all_consultations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all consultation bookings.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ConsultationService(db)

    return service.get_all()


# ============================================================
# USER: CREATE CONSULTATION
# ============================================================

@router.post(
    "",
    response_model=ConsultationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create consultation",
)
def create_consultation(
    request: CreateConsultationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new audio or video consultation booking.

    The consultation is automatically associated with
    the currently authenticated user.
    """

    service = ConsultationService(db)

    try:
        return service.create(
            user_id=str(current_user.id),
            request=request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# USER: GET MY CONSULTATIONS
# ============================================================

@router.get(
    "/me",
    response_model=list[ConsultationResponse],
    summary="Get my consultations",
)
def get_my_consultations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get consultation bookings belonging to
    the currently authenticated user.
    """

    service = ConsultationService(db)

    return service.get_by_user_id(
        str(current_user.id)
    )


# ============================================================
# ADMIN: GET CONSULTATIONS BY STATUS
# ============================================================

@router.get(
    "/status/{consultation_status}",
    response_model=list[ConsultationResponse],
    summary="Get consultations by status",
)
def get_consultations_by_status(
    consultation_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get consultation bookings filtered by status.

    Example statuses:

    PENDING
    CONFIRMED
    IN_PROGRESS
    COMPLETED
    CANCELLED
    """

    service = ConsultationService(db)

    return service.get_by_status(
        consultation_status
    )


# ============================================================
# GET CONSULTATIONS BY TYPE
# ============================================================

@router.get(
    "/type/{consultation_type}",
    response_model=list[ConsultationResponse],
    summary="Get consultations by type",
)
def get_consultations_by_type(
    consultation_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get consultations filtered by consultation type.

    Supported examples:

    AUDIO
    VIDEO
    """

    service = ConsultationService(db)

    return service.get_by_type(
        consultation_type
    )


# ============================================================
# ADMIN: GET CONSULTATIONS BY PRIEST
# ============================================================

@router.get(
    "/priest/{priest_id}",
    response_model=list[ConsultationResponse],
    summary="Get consultations by priest ID",
)
def get_consultations_by_priest(
    priest_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all consultations assigned to a specific priest.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ConsultationService(db)

    return service.get_by_priest_id(
        priest_id
    )


# ============================================================
# GET CONSULTATIONS BY KUNDLI
# ============================================================

@router.get(
    "/kundli/{kundli_id}",
    response_model=list[ConsultationResponse],
    summary="Get consultations by Kundli ID",
)
def get_consultations_by_kundli(
    kundli_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get consultations linked to a Kundli request.
    """

    service = ConsultationService(db)

    return service.get_by_kundli_id(
        kundli_id
    )


# ============================================================
# GET CONSULTATION BY ID
# ============================================================

@router.get(
    "/{consultation_id}",
    response_model=ConsultationResponse,
    summary="Get consultation by ID",
)
def get_consultation(
    consultation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a consultation booking by ID.
    """

    service = ConsultationService(db)

    try:
        consultation = service.get_by_id(
            consultation_id
        )

        # Users can access only their own consultation.
        # Admins and Super Admins can access any consultation.
        if (
            str(consultation.user_id) != str(current_user.id)
            and current_user.role.name
            not in ("ADMIN", "SUPER_ADMIN")
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this consultation.",
            )

        return consultation

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# USER: UPDATE OWN CONSULTATION
# ============================================================

@router.put(
    "/{consultation_id}",
    response_model=ConsultationResponse,
    summary="Update my consultation",
)
def update_consultation(
    consultation_id: str,
    request: UpdateConsultationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a consultation belonging to
    the currently authenticated user.
    """

    service = ConsultationService(db)

    try:
        consultation = service.get_by_id(
            consultation_id
        )

        if str(consultation.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this consultation.",
            )

        return service.update(
            consultation_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# ADMIN: MANAGE CONSULTATION
# ============================================================

@router.patch(
    "/{consultation_id}/manage",
    response_model=ConsultationResponse,
    summary="Manage consultation",
)
def manage_consultation(
    consultation_id: str,
    request: ManageConsultationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Manage a consultation booking.

    ADMIN and SUPER_ADMIN can use this endpoint to:

    - Assign a priest
    - Change consultation status
    - Set meeting URL
    - Set meeting ID
    - Add administrative notes
    - Manage consultation scheduling
    """

    service = ConsultationService(db)

    try:
        return service.manage(
            consultation_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# USER: CANCEL OWN CONSULTATION
# ============================================================

@router.patch(
    "/{consultation_id}/cancel",
    response_model=ConsultationResponse,
    summary="Cancel my consultation",
)
def cancel_consultation(
    consultation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel a consultation belonging to
    the currently authenticated user.
    """

    service = ConsultationService(db)

    try:
        consultation = service.get_by_id(
            consultation_id
        )

        if str(consultation.user_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to cancel this consultation.",
            )

        return service.cancel(
            consultation_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# SUPER ADMIN: DELETE CONSULTATION
# ============================================================

@router.delete(
    "/{consultation_id}/admin",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Admin delete consultation",
)
def admin_delete_consultation(
    consultation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Permanently delete a consultation.

    Accessible only to SUPER_ADMIN.
    """

    service = ConsultationService(db)

    try:
        service.delete(
            consultation_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc