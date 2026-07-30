from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    """
    Repository for User database operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_by_id(
        self,
        user_id: str,
    ) -> User | None:
        statement = select(User).where(
            User.id == user_id,
        )
        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = select(User).where(
            User.email == email,
        )
        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[User]:
        statement = select(User).order_by(
            User.full_name.asc(),
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        user: User,
    ) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(
        self,
        user: User,
    ) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(
        self,
        user: User,
    ) -> None:
        self.db.delete(user)
        self.db.commit()