from __future__ import annotations

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.models.user import User
from app.repositories import RoleRepository, UserRepository


ADMIN_EMAIL = "admin@vishwaarpana.com"
ADMIN_PASSWORD = "Admin@123"
ADMIN_NAME = "System Administrator"
ADMIN_MOBILE = "9999999999"


def seed() -> None:
    db = SessionLocal()

    try:
        user_repository = UserRepository(db)
        role_repository = RoleRepository(db)

        existing_user = user_repository.get_by_email(
            ADMIN_EMAIL
        )

        if existing_user is not None:
            print("✓ Admin user already exists.")
            return

        admin_role = role_repository.get_by_name(
            "ADMIN"
        )

        if admin_role is None:
            raise Exception(
                "ADMIN role not found. Run seed_roles first."
            )

        admin = User(
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            mobile=ADMIN_MOBILE,
            password_hash=hash_password(
                ADMIN_PASSWORD
            ),
            role_id=admin_role.id,
            is_active=True,
            is_verified=True,
        )

        user_repository.create(admin)

        print("✓ Admin user created successfully.")
        print(f"Email    : {ADMIN_EMAIL}")
        print(f"Password : {ADMIN_PASSWORD}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()