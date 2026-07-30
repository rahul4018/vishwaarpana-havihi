from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateCategoryRequest(BaseModel):
    """
    Request schema for creating a category.
    """

    temple_id: UUID

    name: str = Field(
        min_length=2,
        max_length=150,
        examples=["Archana"],
    )

    slug: str = Field(
        min_length=2,
        max_length=150,
        examples=["archana"],
    )

    description: str | None = Field(
        default=None,
        examples=["Daily Archana services"],
    )

    display_order: int = Field(
        default=1,
        ge=1,
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class UpdateCategoryRequest(BaseModel):
    """
    Request schema for updating a category.
    """

    name: str | None = Field(
        default=None,
        max_length=150,
    )

    slug: str | None = Field(
        default=None,
        max_length=150,
    )

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=1,
    )

    is_active: bool | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class CategoryResponse(BaseModel):
    """
    Category response schema.
    """

    id: UUID
    temple_id: UUID
    name: str
    slug: str
    description: str | None
    display_order: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )