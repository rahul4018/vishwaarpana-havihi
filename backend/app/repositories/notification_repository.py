from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.notification import Notification


class NotificationRepository:
    """
    Repository for Notification database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        notification: Notification,
    ) -> Notification:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)

        return notification

    def get_by_id(
        self,
        notification_id: str,
    ) -> Notification | None:
        statement = select(Notification).where(
            Notification.id == notification_id
        )

        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Notification]:
        statement = select(Notification).order_by(
            Notification.created_at.desc()
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[Notification]:
        statement = (
            select(Notification)
            .where(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_unread_by_user_id(
        self,
        user_id: str,
    ) -> list[Notification]:
        statement = (
            select(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .order_by(
                Notification.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        notification: Notification,
    ) -> Notification:
        self.db.commit()
        self.db.refresh(notification)

        return notification

    def delete(
        self,
        notification: Notification,
    ) -> None:
        self.db.delete(notification)
        self.db.commit()