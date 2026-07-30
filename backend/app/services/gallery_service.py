from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.gallery import Gallery
from app.repositories import (
    GalleryRepository,
    PoojaRepository,
    TempleRepository,
)
from app.schemas import (
    CreateGalleryRequest,
    GalleryResponse,
    UpdateGalleryRequest,
)


class GalleryService:
    """
    Gallery business logic.
    """

    def __init__(self, db: Session) -> None:
        self.gallery_repository = GalleryRepository(db)
        self.temple_repository = TempleRepository(db)
        self.pooja_repository = PoojaRepository(db)

    def create(
        self,
        request: CreateGalleryRequest,
    ) -> GalleryResponse:

        if request.temple_id is not None:
            temple = self.temple_repository.get_by_id(
                str(request.temple_id)
            )

            if temple is None:
                raise ResourceNotFoundError(
                    "Temple not found."
                )

        if request.pooja_id is not None:
            pooja = self.pooja_repository.get_by_id(
                str(request.pooja_id)
            )

            if pooja is None:
                raise ResourceNotFoundError(
                    "Pooja not found."
                )

        gallery = Gallery(
            temple_id=request.temple_id,
            pooja_id=request.pooja_id,
            title=request.title,
            description=request.description,
            image_url=request.image_url,
            display_order=request.display_order,
            is_active=request.is_active,
        )

        created = self.gallery_repository.create(
            gallery
        )

        return GalleryResponse.model_validate(
            created
        )

    def get_all(self) -> list[GalleryResponse]:

        gallery_items = self.gallery_repository.get_all()

        return [
            GalleryResponse.model_validate(item)
            for item in gallery_items
        ]

    def get_by_id(
        self,
        gallery_id: str,
    ) -> GalleryResponse:

        gallery = self.gallery_repository.get_by_id(
            gallery_id
        )

        if gallery is None:
            raise ResourceNotFoundError(
                "Gallery item not found."
            )

        return GalleryResponse.model_validate(
            gallery
        )

    def get_by_temple_id(
        self,
        temple_id: str,
    ) -> list[GalleryResponse]:

        temple = self.temple_repository.get_by_id(
            temple_id
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        gallery_items = (
            self.gallery_repository.get_by_temple_id(
                temple_id
            )
        )

        return [
            GalleryResponse.model_validate(item)
            for item in gallery_items
        ]

    def get_by_pooja_id(
        self,
        pooja_id: str,
    ) -> list[GalleryResponse]:

        pooja = self.pooja_repository.get_by_id(
            pooja_id
        )

        if pooja is None:
            raise ResourceNotFoundError(
                "Pooja not found."
            )

        gallery_items = (
            self.gallery_repository.get_by_pooja_id(
                pooja_id
            )
        )

        return [
            GalleryResponse.model_validate(item)
            for item in gallery_items
        ]

    def update(
        self,
        gallery_id: str,
        request: UpdateGalleryRequest,
    ) -> GalleryResponse:

        gallery = self.gallery_repository.get_by_id(
            gallery_id
        )

        if gallery is None:
            raise ResourceNotFoundError(
                "Gallery item not found."
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "temple_id" in update_data:
            temple_id = update_data["temple_id"]

            if temple_id is not None:
                temple = self.temple_repository.get_by_id(
                    str(temple_id)
                )

                if temple is None:
                    raise ResourceNotFoundError(
                        "Temple not found."
                    )

        if "pooja_id" in update_data:
            pooja_id = update_data["pooja_id"]

            if pooja_id is not None:
                pooja = self.pooja_repository.get_by_id(
                    str(pooja_id)
                )

                if pooja is None:
                    raise ResourceNotFoundError(
                        "Pooja not found."
                    )

        for field, value in update_data.items():
            setattr(
                gallery,
                field,
                value,
            )

        updated = self.gallery_repository.update(
            gallery
        )

        return GalleryResponse.model_validate(
            updated
        )

    def delete(
        self,
        gallery_id: str,
    ) -> None:

        gallery = self.gallery_repository.get_by_id(
            gallery_id
        )

        if gallery is None:
            raise ResourceNotFoundError(
                "Gallery item not found."
            )

        self.gallery_repository.delete(
            gallery
        )