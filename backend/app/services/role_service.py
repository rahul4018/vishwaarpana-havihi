from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import RoleRepository
from app.schemas import RoleResponse


class RoleService:
    """
    Role business logic.
    """

    def __init__(self, db: Session) -> None:
        self.role_repository = RoleRepository(db)

    def get_all(self) -> list[RoleResponse]:
        roles = self.role_repository.get_all()

        return [
            RoleResponse.model_validate(role)
            for role in roles
        ]