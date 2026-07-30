from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateTempleRequest(BaseModel):
    """
    Request schema for creating a temple.
    """

    name: str = Field(
        min_length=2,
        max_length=255,
        examples=["ISKCON Bangalore"],
    )

    slug: str = Field(
        min_length=2,
        max_length=255,
        examples=["iskcon-bangalore"],
    )

    description: str | None = Field(
        default=None,
        examples=["One of the largest ISKCON temples in India."],
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=20,
        examples=["9876543210"],
    )

    website: str | None = Field(
        default=None,
        max_length=255,
        examples=["https://www.iskconbangalore.org"],
    )

    address: str = Field(
        min_length=5,
        examples=["Rajajinagar, Bengaluru"],
    )

    city: str = Field(
        max_length=100,
        examples=["Bengaluru"],
    )

    state: str = Field(
        max_length=100,
        examples=["Karnataka"],
    )

    country: str = Field(
        default="India",
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        max_length=20,
        examples=["560010"],
    )

    latitude: str | None = Field(
        default=None,
        max_length=50,
        examples=["12.9716"],
    )

    longitude: str | None = Field(
        default=None,
        max_length=50,
        examples=["77.5946"],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class UpdateTempleRequest(BaseModel):
    """
    Request schema for updating a temple.
    """

    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    website: str | None = Field(default=None, max_length=255)
    address: str | None = None
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    latitude: str | None = Field(default=None, max_length=50)
    longitude: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class TempleResponse(BaseModel):
    """
    Temple response schema.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    name: str
    slug: str
    description: str | None
    email: EmailStr | None
    phone: str | None
    website: str | None
    address: str
    city: str
    state: str
    country: str
    postal_code: str | None
    latitude: str | None
    longitude: str | None
    is_active: bool