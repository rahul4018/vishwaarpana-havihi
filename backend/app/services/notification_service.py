from __future__ import annotations

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.notification import Notification
from app.repositories import NotificationRepository, UserRepository
from app.schemas import (
    CreateNotificationRequest,
    NotificationResponse,
    UpdateNotificationRequest,
)


class NotificationService:
    """
    Notification business logic.
    """

    def __init__(self, db) -> None:
        self.notification_repository = NotificationRepository(db)
        self.user_repository = UserRepository(db)

    def create(
        self,
        request: CreateNotificationRequest,
    ) -> NotificationResponse:
        """
        Create a notification for a user.
        """

        user = self.user_repository.get_by_id(
            str(request.user_id)
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found."
            )

        notification = Notification(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=request.notification_type,
            reference_id=request.reference_id,
        )

        created = self.notification_repository.create(
            notification
        )

        return NotificationResponse.model_validate(
            created
        )

    def get_all(
        self,
    ) -> list[NotificationResponse]:
        """
        Get all notifications.
        """

        notifications = (
            self.notification_repository.get_all()
        )

        return [
            NotificationResponse.model_validate(
                notification
            )
            for notification in notifications
        ]

    def get_by_id(
        self,
        notification_id: str,
    ) -> NotificationResponse:
        """
        Get a notification by ID.
        """

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ResourceNotFoundError(
                "Notification not found."
            )

        return NotificationResponse.model_validate(
            notification
        )

    def get_by_user_id(
        self,
        user_id: str,
    ) -> list[NotificationResponse]:
        """
        Get all notifications for a user.
        """

        notifications = (
            self.notification_repository.get_by_user_id(
                user_id
            )
        )

        return [
            NotificationResponse.model_validate(
                notification
            )
            for notification in notifications
        ]

    def get_unread_by_user_id(
        self,
        user_id: str,
    ) -> list[NotificationResponse]:
        """
        Get unread notifications for a user.
        """

        notifications = (
            self.notification_repository
            .get_unread_by_user_id(
                user_id
            )
        )

        return [
            NotificationResponse.model_validate(
                notification
            )
            for notification in notifications
        ]

    def mark_as_read(
        self,
        notification_id: str,
    ) -> NotificationResponse:
        """
        Mark a notification as read.
        """

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ResourceNotFoundError(
                "Notification not found."
            )

        notification.is_read = True

        updated = self.notification_repository.update(
            notification
        )

        return NotificationResponse.model_validate(
            updated
        )

    def update(
        self,
        notification_id: str,
        request: UpdateNotificationRequest,
    ) -> NotificationResponse:
        """
        Update a notification.
        """

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ResourceNotFoundError(
                "Notification not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                notification,
                field,
                value,
            )

        updated = self.notification_repository.update(
            notification
        )

        return NotificationResponse.model_validate(
            updated
        )

    def delete(
        self,
        notification_id: str,
    ) -> None:
        """
        Delete a notification.
        """

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ResourceNotFoundError(
                "Notification not found."
            )

        self.notification_repository.delete(
            notification
        )