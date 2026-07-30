from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    ContactResponse,
    CreateContactRequest,
    UpdateContactRequest,
)
from app.services import ContactService


router = APIRouter(
    prefix="/contacts",
    tags=["Contact"],
)


@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit contact enquiry",
)
def create_contact(
    request: CreateContactRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a new contact enquiry.
    This endpoint is public.
    """

    service = ContactService(db)

    return service.create(request)


@router.get(
    "",
    response_model=list[ContactResponse],
    summary="Get all contact enquiries",
)
def get_all_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all contact enquiries.
    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ContactService(db)

    return service.get_all()


@router.get(
    "/status/{enquiry_status}",
    response_model=list[ContactResponse],
    summary="Get contact enquiries by status",
)
def get_contacts_by_status(
    enquiry_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get contact enquiries filtered by status.
    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ContactService(db)

    return service.get_by_status(enquiry_status)


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    summary="Get contact enquiry by ID",
)
def get_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get a contact enquiry by ID.
    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ContactService(db)

    try:
        return service.get_by_id(contact_id)

    except (ResourceNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    summary="Update contact enquiry",
)
def update_contact(
    contact_id: str,
    request: UpdateContactRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Update enquiry status or admin notes.
    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ContactService(db)

    try:
        return service.update(
            contact_id,
            request,
        )

    except (ResourceNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete contact enquiry",
)
def delete_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Delete a contact enquiry.
    Accessible only to SUPER_ADMIN.
    """

    service = ContactService(db)

    try:
        service.delete(contact_id)

    except (ResourceNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc