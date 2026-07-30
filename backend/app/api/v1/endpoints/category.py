from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import (
    DuplicateCategoryNameError,
    DuplicateCategorySlugError,
    ResourceNotFoundError,
)
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)
from app.services import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Category"],
)


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="List categories",
)
def get_categories(
    db: Session = Depends(get_db),
):
    service = CategoryService(db)
    return service.get_all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get category",
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    try:
        return service.get_by_id(category_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
)
def create_category(
    request: CreateCategoryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = CategoryService(db)

    try:
        return service.create(request)

    except DuplicateCategoryNameError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except DuplicateCategorySlugError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update category",
)
def update_category(
    category_id: str,
    request: UpdateCategoryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    service = CategoryService(db)

    try:
        return service.update(category_id, request)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    service = CategoryService(db)

    try:
        service.delete(category_id)

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc