from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import RoleRepository, UserRepository


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)