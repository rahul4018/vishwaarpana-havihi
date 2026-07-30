from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.temple import Temple


class TempleRepository:
    """
    Repository for Temple database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, temple_id: str) -> Temple | None:
        statement = select(Temple).where(
            Temple.id == temple_id,
        )
        return self.db.scalar(statement)

    def get_by_name(self, name: str) -> Temple | None:
        statement = select(Temple).where(
            Temple.name == name,
        )
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Temple | None:
        statement = select(Temple).where(
            Temple.slug == slug,
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Temple]:
        statement = select(Temple).order_by(
            Temple.name.asc(),
        )
        return list(self.db.scalars(statement).all())

    def create(self, temple: Temple) -> Temple:
        self.db.add(temple)
        self.db.commit()
        self.db.refresh(temple)
        return temple

    def update(self, temple: Temple) -> Temple:
        self.db.commit()
        self.db.refresh(temple)
        return temple

    def delete(self, temple: Temple) -> None:
        self.db.delete(temple)
        self.db.commit()