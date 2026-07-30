from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.pooja import Pooja


class PoojaRepository:
    """
    Repository for Pooja database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        pooja_id: str,
    ) -> Pooja | None:
        statement = select(Pooja).where(
            Pooja.id == pooja_id,
        )
        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Pooja | None:
        statement = select(Pooja).where(
            Pooja.slug == slug,
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Pooja]:
        statement = (
            select(Pooja)
            .order_by(Pooja.name.asc())
        )
        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        pooja: Pooja,
    ) -> Pooja:
        try:
            self.db.add(pooja)
            self.db.commit()
            self.db.refresh(pooja)
            return pooja

        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pooja with this slug already exists.",
            ) from exc

    def update(
        self,
        pooja: Pooja,
    ) -> Pooja:
        try:
            self.db.commit()
            self.db.refresh(pooja)
            return pooja

        except IntegrityError as exc:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pooja with this slug already exists.",
            ) from exc

    def delete(
        self,
        pooja: Pooja,
    ) -> None:
        self.db.delete(pooja)
        self.db.commit()