from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.category import Category


class CategoryRepository:
    """
    Repository for Category database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        category_id: str,
    ) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id,
        )
        return self.db.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> Category | None:
        statement = select(Category).where(
            Category.name == name,
        )
        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Category | None:
        statement = select(Category).where(
            Category.slug == slug,
        )
        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Category]:
        statement = select(Category).order_by(
            Category.display_order.asc(),
            Category.name.asc(),
        )
        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        category: Category,
    ) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(
        self,
        category: Category,
    ) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(
        self,
        category: Category,
    ) -> None:
        self.db.delete(category)
        self.db.commit()