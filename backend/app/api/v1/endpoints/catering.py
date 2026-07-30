from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CateringResponse,
    CreateCateringRequest,
    UpdateCateringRequest,
)
from app.services import CateringService


router = APIRouter(
    prefix="/catering",
    tags=["Catering"],
)


@router.get(
    "",
    response_model=list[CateringResponse],
    summary="Get all catering and prasadam services",
)
def get_all_catering_services(
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    return service.get_all()


@router.get(
    "/available",
    response_model=list[CateringResponse],
    summary="Get available catering and prasadam services",
)
def get_available_catering_services(
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    return service.get_available()


@router.get(
    "/type/{service_type}",
    response_model=list[CateringResponse],
    summary="Get services by type",
)
def get_catering_by_service_type(
    service_type: str,
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    try:
        return service.get_by_service_type(
            service_type
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/temple/{temple_id}",
    response_model=list[CateringResponse],
    summary="Get catering services by temple ID",
)
def get_catering_by_temple(
    temple_id: str,
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    try:
        return service.get_by_temple_id(
            temple_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/pooja/{pooja_id}",
    response_model=list[CateringResponse],
    summary="Get catering services by pooja ID",
)
def get_catering_by_pooja(
    pooja_id: str,
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    try:
        return service.get_by_pooja_id(
            pooja_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{catering_id}",
    response_model=CateringResponse,
    summary="Get catering service by ID",
)
def get_catering_service(
    catering_id: str,
    db: Session = Depends(get_db),
):
    service = CateringService(db)

    try:
        return service.get_by_id(
            catering_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=CateringResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create catering or prasadam service",
)
def create_catering_service(
    request: CreateCateringRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = CateringService(db)

    try:
        return service.create(
            request
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


@router.put(
    "/{catering_id}",
    response_model=CateringResponse,
    summary="Update catering or prasadam service",
)
def update_catering_service(
    catering_id: str,
    request: UpdateCateringRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = CateringService(db)

    try:
        return service.update(
            catering_id,
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
    "/{catering_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete catering or prasadam service",
)
def delete_catering_service(
    catering_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    service = CateringService(db)

    try:
        service.delete(
            catering_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc