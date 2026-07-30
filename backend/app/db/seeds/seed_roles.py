from __future__ import annotations

from app.db.database import SessionLocal
from app.db.models.role import Role
from app.repositories import RoleRepository


ROLES = [
    ("ADMIN", "System Administrator"),
    ("CUSTOMER", "Customer"),
    ("PRIEST", "Priest"),
    ("MANAGER", "Manager"),
]


def seed() -> None:
    db = SessionLocal()

    try:
        role_repository = RoleRepository(db)

        for name, description in ROLES:
            existing = role_repository.get_by_name(name)

            if existing is None:
                role = Role(
                    name=name,
                    description=description,
                )
                role_repository.create(role)
                print(f"✓ Created role: {name}")
            else:
                print(f"• Role already exists: {name}")

        db.commit()
        print("✓ Roles seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()