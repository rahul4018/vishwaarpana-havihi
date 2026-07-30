from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateKundliRequest,
    KundliResponse,
    ManageKundliRequest,
    UpdateKundliRequest,
)
from app.services import KundliService


router = APIRouter(
    prefix="/kundli",
    tags=["Kundli"],
)


@router.get(
    "",
    response_model=list[KundliResponse],
    summary="Get all Kundli requests",
)
def get_all_kundli_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all Kundli and astrology service requests.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = KundliService(db)

    return service.get_all()


@router.get(
    "/me",
    response_model=list[KundliResponse],
    summary="Get my Kundli requests",
)
def get_my_kundli_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get Kundli requests created by the current user.
    """

    service = KundliService(db)

    return service.get_by_user_id(
        str(current_user.id)
    )


@router.get(
    "/status/{request_status}",
    response_model=list[KundliResponse],
    summary="Get Kundli requests by status",
)
def get_kundli_requests_by_status(
    request_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get Kundli requests filtered by status.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = KundliService(db)

    try:
        return service.get_by_status(
            request_status
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/priest/{priest_id}",
    response_model=list[KundliResponse],
    summary="Get Kundli requests by priest ID",
)
def get_kundli_requests_by_priest(
    priest_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get Kundli requests assigned to a priest.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = KundliService(db)

    try:
        return service.get_by_priest_id(
            priest_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=KundliResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Kundli request",
)
def create_kundli_request(
    request: CreateKundliRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a Kundli, horoscope, matchmaking,
    or astrology consultation request.
    """

    service = KundliService(db)

    try:
        return service.create(
            str(current_user.id),
            request,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{kundli_id}",
    response_model=KundliResponse,
    summary="Get Kundli request by ID",
)
def get_kundli_request(
    kundli_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a Kundli request by ID.
    """

    service = KundliService(db)

    try:
        kundli = service.get_by_id(
            kundli_id
        )

        # Normal users can only access their own request.
        # Admins and super admins can access all requests.
        user_role = str(current_user.role).upper()

        if (
            kundli.user_id != current_user.id
            and user_role not in {
                "ADMIN",
                "SUPER_ADMIN",
            }
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this Kundli request.",
            )

        return kundli

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{kundli_id}",
    response_model=KundliResponse,
    summary="Update my Kundli request",
)
def update_kundli_request(
    kundli_id: str,
    request: UpdateKundliRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a Kundli request owned by the current user.
    """

    service = KundliService(db)

    try:
        return service.update_owned(
            kundli_id,
            str(current_user.id),
            request,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{kundli_id}/manage",
    response_model=KundliResponse,
    summary="Manage Kundli request",
)
def manage_kundli_request(
    kundli_id: str,
    request: ManageKundliRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Manage a Kundli request.

    Allows administrators to assign a priest,
    update status, attach report URL,
    and add administrative notes.
    """

    service = KundliService(db)

    try:
        return service.manage(
            kundli_id,
            request,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{kundli_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete my Kundli request",
)
def delete_kundli_request(
    kundli_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a Kundli request owned by the current user.
    """

    service = KundliService(db)

    try:
        service.delete_owned(
            kundli_id,
            str(current_user.id),
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{kundli_id}/admin",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Admin delete Kundli request",
)
def admin_delete_kundli_request(
    kundli_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Permanently delete any Kundli request.

    Accessible only to SUPER_ADMIN.
    """

    service = KundliService(db)

    try:
        service.delete(
            kundli_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc