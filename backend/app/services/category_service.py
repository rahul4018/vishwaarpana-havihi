from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import (
    DuplicateCategoryNameError,
    DuplicateCategorySlugError,
    ResourceNotFoundError,
)
from app.db.models.category import Category
from app.repositories import CategoryRepository
from app.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)


class CategoryService:
    """
    Category business logic.
    """

    def __init__(self, db: Session) -> None:
        self.category_repository = CategoryRepository(db)

    def create(
        self,
        request: CreateCategoryRequest,
    ) -> CategoryResponse:
        """
        Create a new category.
        """

        if self.category_repository.get_by_name(request.name):
            raise DuplicateCategoryNameError(
                "Category name already exists."
            )

        if self.category_repository.get_by_slug(request.slug):
            raise DuplicateCategorySlugError(
                "Category slug already exists."
            )

        category = Category(
            temple_id=request.temple_id,
            name=request.name,
            slug=request.slug,
            description=request.description,
            display_order=request.display_order,
            is_active=True,
        )

        created = self.category_repository.create(category)

        return CategoryResponse.model_validate(created)

    def get_by_id(
        self,
        category_id: str,
    ) -> CategoryResponse:
        """
        Get category by ID.
        """

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError(
                "Category not found."
            )

        return CategoryResponse.model_validate(category)

    def get_all(
        self,
    ) -> list[CategoryResponse]:
        """
        Get all categories.
        """

        categories = self.category_repository.get_all()

        return [
            CategoryResponse.model_validate(category)
            for category in categories
        ]

    def update(
        self,
        category_id: str,
        request: UpdateCategoryRequest,
    ) -> CategoryResponse:
        """
        Update an existing category.
        """

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError(
                "Category not found."
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(category, field, value)

        updated = self.category_repository.update(category)

        return CategoryResponse.model_validate(updated)

    def delete(
        self,
        category_id: str,
    ) -> None:
        """
        Delete a category.
        """

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError(
                "Category not found."
            )

        self.category_repository.delete(category)