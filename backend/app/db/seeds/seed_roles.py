from __future__ import annotations

from app.db.database import SessionLocal
from app.db.models.role import Role
from app.repositories import RoleRepository

DEFAULT_ROLES: list[tuple[str, str]] = [
    (
        "SUPER_ADMIN",
        "System Super Administrator",
    ),
    (
        "ADMIN",
        "Temple Administrator",
    ),
    (
        "PRIEST",
        "Temple Priest",
    ),
    (
        "DEVOTEE",
        "Registered Devotee",
    ),
]


def seed() -> None:
    """
    Seed default RBAC roles into the database.
    Safe to execute multiple times.
    """
    db = SessionLocal()

    try:
        repository = RoleRepository(db)

        for role_name, description in DEFAULT_ROLES:
            existing_role = repository.get_by_name(role_name)

            if existing_role is not None:
                print(f"✓ {role_name} already exists")
                continue

            role = Role(
                name=role_name,
                description=description,
                is_active=True,
            )

            repository.create(role)

            print(f"✓ {role_name} created")

        print("\n✓ Default roles seeded successfully.")

    except Exception as exc:
        db.rollback()
        print(f"\n✗ Seeding failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()