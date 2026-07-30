from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateReviewRequest,
    ModerateReviewRequest,
    ReviewResponse,
    UpdateReviewRequest,
)
from app.services import ReviewService


router = APIRouter(
    prefix="/reviews",
    tags=["Review"],
)


@router.get(
    "",
    response_model=list[ReviewResponse],
    summary="Get all reviews",
)
def get_all_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all reviews.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ReviewService(db)

    return service.get_all()


@router.get(
    "/me",
    response_model=list[ReviewResponse],
    summary="Get my reviews",
)
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get reviews submitted by the currently
    authenticated user.
    """

    service = ReviewService(db)

    return service.get_by_user_id(
        str(current_user.id)
    )


@router.get(
    "/pooja/{pooja_id}",
    response_model=list[ReviewResponse],
    summary="Get approved reviews by pooja ID",
)
def get_reviews_by_pooja(
    pooja_id: str,
    db: Session = Depends(get_db),
):
    """
    Get publicly visible approved reviews
    for a specific pooja.
    """

    service = ReviewService(db)

    try:
        return service.get_approved_by_pooja_id(
            pooja_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Get review by ID",
)
def get_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get a review by ID.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ReviewService(db)

    try:
        return service.get_by_id(
            review_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create review",
)
def create_review(
    request: CreateReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a review for a completed booking.

    The authenticated user must own the booking.
    """

    service = ReviewService(db)

    try:
        return service.create(
            request,
            current_user.id,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Update my review",
)
def update_review(
    review_id: str,
    request: UpdateReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a review owned by the authenticated user.

    Updating a review resets its moderation
    status to PENDING.
    """

    service = ReviewService(db)

    try:
        return service.update(
            review_id,
            request,
            current_user.id,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{review_id}/moderate",
    response_model=ReviewResponse,
    summary="Moderate review",
)
def moderate_review(
    review_id: str,
    request: ModerateReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Approve or reject a review.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = ReviewService(db)

    try:
        return service.moderate(
            review_id,
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
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete review",
)
def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Delete a review.

    Accessible only to SUPER_ADMIN.
    """

    service = ReviewService(db)

    try:
        service.delete(
            review_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc