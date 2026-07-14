from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.role import Role


class RoleRepository:
    """
    Repository for Role database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return self.db.scalar(statement)