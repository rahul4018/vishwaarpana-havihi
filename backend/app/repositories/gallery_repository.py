from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.gallery import Gallery


class GalleryRepository:
    """
    Repository for Gallery database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        gallery: Gallery,
    ) -> Gallery:
        self.db.add(gallery)
        self.db.commit()
        self.db.refresh(gallery)
        return gallery

    def get_by_id(
        self,
        gallery_id: str,
    ) -> Gallery | None:
        statement = select(Gallery).where(
            Gallery.id == gallery_id
        )

        return self.db.scalar(statement)

    def get_all(
        self,
    ) -> list[Gallery]:
        statement = select(Gallery).order_by(
            Gallery.created_at.desc()
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_temple_id(
        self,
        temple_id: str,
    ) -> list[Gallery]:
        statement = (
            select(Gallery)
            .where(
                Gallery.temple_id == temple_id
            )
            .order_by(
                Gallery.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[Gallery]:
        statement = (
            select(Gallery)
            .where(
                Gallery.pooja_id == pooja_id
            )
            .order_by(
                Gallery.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        gallery: Gallery,
    ) -> Gallery:
        self.db.commit()
        self.db.refresh(gallery)
        return gallery

    def delete(
        self,
        gallery: Gallery,
    ) -> None:
        self.db.delete(gallery)
        self.db.commit()