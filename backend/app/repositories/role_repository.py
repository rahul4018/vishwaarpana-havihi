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

    def get_all(self) -> list[Role]:
        statement = select(Role).order_by(Role.name)
        return list(self.db.scalars(statement).all())

    def create(self, role: Role) -> Role:
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role