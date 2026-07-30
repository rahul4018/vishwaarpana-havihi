from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.dependencies.auth import get_current_user
from app.db.models.user import User


def require_roles(
    *roles: str,
) -> Callable[..., User]:
    """
    Require one of the specified roles.
    """

    def permission(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return permission


require_super_admin = require_roles(
    "SUPER_ADMIN",
)

require_admin = require_roles(
    "SUPER_ADMIN",
    "ADMIN",
)

require_priest = require_roles(
    "SUPER_ADMIN",
    "ADMIN",
    "PRIEST",
)

require_devotee = require_roles(
    "SUPER_ADMIN",
    "ADMIN",
    "PRIEST",
    "DEVOTEE",
)