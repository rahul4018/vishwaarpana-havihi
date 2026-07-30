from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.review import Review
from app.repositories import (
    BookingRepository,
    PoojaRepository,
    ReviewRepository,
)
from app.schemas import (
    CreateReviewRequest,
    ModerateReviewRequest,
    ReviewResponse,
    UpdateReviewRequest,
)


class ReviewService:
    """
    Review business logic.
    """

    def __init__(self, db: Session) -> None:
        self.review_repository = ReviewRepository(db)
        self.booking_repository = BookingRepository(db)
        self.pooja_repository = PoojaRepository(db)

    def create(
        self,
        request: CreateReviewRequest,
        user_id,
    ) -> ReviewResponse:
        """
        Create a review for a booking.
        """

        booking = self.booking_repository.get_by_id(
            str(request.booking_id)
        )

        if booking is None:
            raise ResourceNotFoundError(
                "Booking not found."
            )

        if str(booking.user_id) != str(user_id):
            raise PermissionError(
                "You can only review your own booking."
            )

        if str(booking.pooja_id) != str(request.pooja_id):
            raise ValueError(
                "The selected pooja does not match the booking."
            )

        pooja = self.pooja_repository.get_by_id(
            str(request.pooja_id)
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        existing_review = (
            self.review_repository.get_by_booking_id(
                str(request.booking_id)
            )
        )

        if existing_review is not None:
            raise ValueError(
                "A review already exists for this booking."
            )

        booking_status = str(
            booking.booking_status
        ).upper()

        if booking_status != "COMPLETED":
            raise ValueError(
                "You can review only a completed booking."
            )

        review = Review(
            user_id=user_id,
            booking_id=request.booking_id,
            pooja_id=request.pooja_id,
            rating=request.rating,
            review_text=request.review_text,
            review_status="PENDING",
        )

        created = self.review_repository.create(
            review
        )

        return ReviewResponse.model_validate(
            created
        )

    def get_all(
        self,
    ) -> list[ReviewResponse]:
        """
        Get all reviews.
        """

        reviews = self.review_repository.get_all()

        return [
            ReviewResponse.model_validate(review)
            for review in reviews
        ]

    def get_by_id(
        self,
        review_id: str,
    ) -> ReviewResponse:
        """
        Get a review by ID.
        """

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ResourceNotFoundError(
                "Review not found."
            )

        return ReviewResponse.model_validate(
            review
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[ReviewResponse]:
        """
        Get reviews submitted by a user.
        """

        reviews = (
            self.review_repository.get_by_user_id(
                user_id
            )
        )

        return [
            ReviewResponse.model_validate(review)
            for review in reviews
        ]

    def get_approved_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[ReviewResponse]:
        """
        Get publicly visible approved reviews
        for a pooja.
        """

        pooja = self.pooja_repository.get_by_id(
            pooja_id
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        reviews = (
            self.review_repository
            .get_approved_by_pooja_id(
                pooja_id
            )
        )

        return [
            ReviewResponse.model_validate(review)
            for review in reviews
        ]

    def update(
        self,
        review_id: str,
        request: UpdateReviewRequest,
        user_id,
    ) -> ReviewResponse:
        """
        Update a review owned by the user.

        Updating a review sends it back
        to pending moderation.
        """

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ResourceNotFoundError(
                "Review not found."
            )

        if str(review.user_id) != str(user_id):
            raise PermissionError(
                "You can only update your own review."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                review,
                field,
                value,
            )

        review.review_status = "PENDING"

        updated = self.review_repository.update(
            review
        )

        return ReviewResponse.model_validate(
            updated
        )

    def moderate(
        self,
        review_id: str,
        request: ModerateReviewRequest,
    ) -> ReviewResponse:
        """
        Approve, reject, or modify moderation
        information for a review.
        """

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ResourceNotFoundError(
                "Review not found."
            )

        allowed_statuses = {
            "PENDING",
            "APPROVED",
            "REJECTED",
        }

        review_status = request.review_status.upper()

        if review_status not in allowed_statuses:
            raise ValueError(
                "Review status must be PENDING, "
                "APPROVED, or REJECTED."
            )

        review.review_status = review_status
        review.admin_response = (
            request.admin_response
        )

        updated = self.review_repository.update(
            review
        )

        return ReviewResponse.model_validate(
            updated
        )

    def delete(
        self,
        review_id: str,
    ) -> None:
        """
        Delete a review.
        """

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ResourceNotFoundError(
                "Review not found."
            )

        self.review_repository.delete(
            review
        )