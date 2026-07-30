from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreatePoojaRequest,
    PoojaResponse,
    UpdatePoojaRequest,
)
from app.services import PoojaService


router = APIRouter(
    prefix="/poojas",
    tags=["Pooja"],
)


@router.get(
    "",
    response_model=list[PoojaResponse],
    summary="List poojas",
)
def get_poojas(
    db: Session = Depends(get_db),
):
    service = PoojaService(db)
    return service.get_all()


@router.get(
    "/{pooja_id}",
    response_model=PoojaResponse,
    summary="Get pooja",
)
def get_pooja(
    pooja_id: str,
    db: Session = Depends(get_db),
):
    service = PoojaService(db)

    try:
        return service.get_by_id(pooja_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=PoojaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create pooja",
)
def create_pooja(
    request: CreatePoojaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN")
    ),
):
    service = PoojaService(db)
    return service.create(request)


@router.put(
    "/{pooja_id}",
    response_model=PoojaResponse,
    summary="Update pooja",
)
def update_pooja(
    pooja_id: str,
    request: UpdatePoojaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN")
    ),
):
    service = PoojaService(db)

    try:
        return service.update(
            pooja_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{pooja_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete pooja",
)
def delete_pooja(
    pooja_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN")
    ),
):
    service = PoojaService(db)

    try:
        service.delete(pooja_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc