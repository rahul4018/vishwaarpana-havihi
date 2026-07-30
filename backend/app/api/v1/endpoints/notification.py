from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateNotificationRequest,
    NotificationResponse,
    UpdateNotificationRequest,
)
from app.services import NotificationService


router = APIRouter(
    prefix="/notifications",
    tags=["Notification"],
)


def _is_notification_owner(
    notification: NotificationResponse,
    current_user: User,
) -> bool:
    """
    Check whether the notification belongs to the current user.
    """

    return str(notification.user_id) == str(current_user.id)


def _get_role_name(
    current_user: User,
) -> str | None:
    """
    Safely retrieve the current user's role name.
    """

    role = getattr(current_user, "role", None)

    if role is None:
        return None

    role_name = getattr(role, "name", None)

    if role_name is None:
        return None

    return str(role_name).upper()


def _is_admin(
    current_user: User,
) -> bool:
    """
    Check whether the current user is an ADMIN or SUPER_ADMIN.
    """

    return _get_role_name(current_user) in {
        "ADMIN",
        "SUPER_ADMIN",
    }


@router.get(
    "",
    response_model=list[NotificationResponse],
    summary="Get all notifications",
)
def get_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get all notifications.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = NotificationService(db)

    return service.get_all()


@router.get(
    "/me",
    response_model=list[NotificationResponse],
    summary="Get my notifications",
)
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get notifications belonging to the current user.
    """

    service = NotificationService(db)

    return service.get_by_user_id(
        str(current_user.id)
    )


@router.get(
    "/me/unread",
    response_model=list[NotificationResponse],
    summary="Get my unread notifications",
)
def get_my_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get unread notifications belonging to the current user.
    """

    service = NotificationService(db)

    return service.get_unread_by_user_id(
        str(current_user.id)
    )


@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse],
    summary="Get notifications by user ID",
)
def get_notifications_by_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Get notifications belonging to a specific user.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = NotificationService(db)

    return service.get_by_user_id(
        user_id
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Get notification by ID",
)
def get_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a notification by ID.

    Normal users can access only their own notifications.
    ADMIN and SUPER_ADMIN can access any notification.
    """

    service = NotificationService(db)

    try:
        notification = service.get_by_id(
            notification_id
        )

        if (
            not _is_notification_owner(
                notification,
                current_user,
            )
            and not _is_admin(current_user)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission to "
                    "access this notification."
                ),
            )

        return notification

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create notification",
)
def create_notification(
    request: CreateNotificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Create a notification for a user.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = NotificationService(db)

    try:
        return service.create(
            request
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Mark notification as read",
)
def mark_notification_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a notification as read.

    Normal users can mark only their own notifications as read.
    ADMIN and SUPER_ADMIN can mark any notification as read.
    """

    service = NotificationService(db)

    try:
        notification = service.get_by_id(
            notification_id
        )

        if (
            not _is_notification_owner(
                notification,
                current_user,
            )
            and not _is_admin(current_user)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission to "
                    "modify this notification."
                ),
            )

        return service.mark_as_read(
            notification_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Update notification",
)
def update_notification(
    notification_id: str,
    request: UpdateNotificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Update a notification.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = NotificationService(db)

    try:
        return service.update(
            notification_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete notification",
)
def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Delete a notification.

    Accessible only to SUPER_ADMIN.
    """

    service = NotificationService(db)

    try:
        service.delete(
            notification_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc