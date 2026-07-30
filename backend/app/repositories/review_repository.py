from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.review import Review


class ReviewRepository:
    """
    Repository for Review database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        review: Review,
    ) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    def get_by_id(
        self,
        review_id: str,
    ) -> Review | None:
        statement = select(Review).where(
            Review.id == review_id
        )

        return self.db.scalar(statement)

    def get_by_booking_id(
        self,
        booking_id: str,
    ) -> Review | None:
        statement = select(Review).where(
            Review.booking_id == booking_id
        )

        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Review]:
        statement = select(Review).order_by(
            Review.created_at.desc()
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[Review]:
        statement = (
            select(Review)
            .where(
                Review.user_id == user_id
            )
            .order_by(
                Review.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[Review]:
        statement = (
            select(Review)
            .where(
                Review.pooja_id == pooja_id
            )
            .order_by(
                Review.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_approved_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[Review]:
        statement = (
            select(Review)
            .where(
                Review.pooja_id == pooja_id,
                Review.review_status == "APPROVED",
            )
            .order_by(
                Review.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        review: Review,
    ) -> Review:
        self.db.commit()
        self.db.refresh(review)

        return review

    def delete(
        self,
        review: Review,
    ) -> None:
        self.db.delete(review)
        self.db.commit()