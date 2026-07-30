from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import (
    DuplicateTempleNameError,
    DuplicateTempleSlugError,
    ResourceNotFoundError,
)
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateTempleRequest,
    TempleResponse,
    UpdateTempleRequest,
)
from app.services import TempleService

router = APIRouter(
    prefix="/temples",
    tags=["Temple"],
)


@router.post(
    "",
    response_model=TempleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create temple",
)
def create_temple(
    request: CreateTempleRequest,
    db: Session = Depends(get_db),
    _: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN")
    ),
) -> TempleResponse:
    service = TempleService(db)

    try:
        return service.create(request)

    except DuplicateTempleNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except DuplicateTempleSlugError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[TempleResponse],
    summary="List temples",
)
def get_temples(
    db: Session = Depends(get_db),
) -> list[TempleResponse]:
    return TempleService(db).get_all()


@router.get(
    "/{temple_id}",
    response_model=TempleResponse,
    summary="Get temple by ID",
)
def get_temple(
    temple_id: str,
    db: Session = Depends(get_db),
) -> TempleResponse:
    try:
        return TempleService(db).get_by_id(
            temple_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/slug/{slug}",
    response_model=TempleResponse,
    summary="Get temple by slug",
)
def get_temple_by_slug(
    slug: str,
    db: Session = Depends(get_db),
) -> TempleResponse:
    try:
        return TempleService(db).get_by_slug(
            slug
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{temple_id}",
    response_model=TempleResponse,
    summary="Update temple",
)
def update_temple(
    temple_id: str,
    request: UpdateTempleRequest,
    db: Session = Depends(get_db),
    _: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN")
    ),
) -> TempleResponse:
    try:
        return TempleService(db).update(
            temple_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{temple_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete temple",
)
def delete_temple(
    temple_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN")
    ),
) -> None:
    try:
        TempleService(db).delete(
            temple_id,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc