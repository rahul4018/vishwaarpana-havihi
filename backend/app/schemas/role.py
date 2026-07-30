from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoleResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(
        from_attributes=True,
    )