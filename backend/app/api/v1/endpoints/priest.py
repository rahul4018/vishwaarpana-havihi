from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreatePriestRequest,
    PriestResponse,
    UpdatePriestRequest,
)
from app.services import PriestService

router = APIRouter(
    prefix="/priests",
    tags=["Priest"],
)


@router.get(
    "",
    response_model=list[PriestResponse],
    summary="List priests",
)
def get_priests(
    db: Session = Depends(get_db),
):
    service = PriestService(db)
    return service.get_all()


@router.get(
    "/{priest_id}",
    response_model=PriestResponse,
    summary="Get priest",
)
def get_priest(
    priest_id: str,
    db: Session = Depends(get_db),
):
    service = PriestService(db)

    try:
        return service.get_by_id(priest_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=PriestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create priest",
)
def create_priest(
    request: CreatePriestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = PriestService(db)
    return service.create(request)


@router.put(
    "/{priest_id}",
    response_model=PriestResponse,
    summary="Update priest",
)
def update_priest(
    priest_id: str,
    request: UpdatePriestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = PriestService(db)

    try:
        return service.update(priest_id, request)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{priest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete priest",
)
def delete_priest(
    priest_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    service = PriestService(db)

    try:
        service.delete(priest_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc