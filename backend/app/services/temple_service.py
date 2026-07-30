from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    DuplicateTempleNameError,
    DuplicateTempleSlugError,
    ResourceNotFoundError,
)
from app.db.models.temple import Temple
from app.repositories import TempleRepository
from app.schemas import (
    CreateTempleRequest,
    TempleResponse,
    UpdateTempleRequest,
)


class TempleService:
    """
    Temple business logic.
    """

    def __init__(self, db: Session) -> None:
        self.temple_repository = TempleRepository(db)

    def create(
        self,
        request: CreateTempleRequest,
    ) -> TempleResponse:
        """
        Create a new temple.
        """

        if self.temple_repository.get_by_name(
            request.name,
        ):
            raise DuplicateTempleNameError(
                "Temple name already exists."
            )

        if self.temple_repository.get_by_slug(
            request.slug,
        ):
            raise DuplicateTempleSlugError(
                "Temple slug already exists."
            )

        temple = Temple(
            name=request.name,
            slug=request.slug,
            description=request.description,
            email=request.email,
            phone=request.phone,
            website=request.website,
            address=request.address,
            city=request.city,
            state=request.state,
            country=request.country,
            postal_code=request.postal_code,
            latitude=request.latitude,
            longitude=request.longitude,
            is_active=True,
        )

        created = self.temple_repository.create(
            temple,
        )

        return TempleResponse.model_validate(created)

    def get_by_id(
        self,
        temple_id: str,
    ) -> TempleResponse:
        """
        Get temple by id.
        """

        temple = self.temple_repository.get_by_id(
            temple_id,
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        return TempleResponse.model_validate(
            temple,
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> TempleResponse:
        """
        Get temple by slug.
        """

        temple = self.temple_repository.get_by_slug(
            slug,
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        return TempleResponse.model_validate(
            temple,
        )

    def get_all(
        self,
    ) -> list[TempleResponse]:
        """
        Get all temples.
        """

        temples = self.temple_repository.get_all()

        return [
            TempleResponse.model_validate(
                temple,
            )
            for temple in temples
        ]

    def update(
        self,
        temple_id: str,
        request: UpdateTempleRequest,
    ) -> TempleResponse:
        """
        Update temple details.
        """

        temple = self.temple_repository.get_by_id(
            temple_id,
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(
                temple,
                field,
                value,
            )

        updated = self.temple_repository.update(
            temple,
        )

        return TempleResponse.model_validate(
            updated,
        )

    def delete(
        self,
        temple_id: str,
    ) -> None:
        """
        Delete a temple.
        """

        temple = self.temple_repository.get_by_id(
            temple_id,
        )

        if temple is None:
            raise ResourceNotFoundError(
                "Temple not found."
            )

        self.temple_repository.delete(
            temple,
        )