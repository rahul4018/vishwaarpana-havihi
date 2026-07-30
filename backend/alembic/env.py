from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.base import Base

# ============================================================
# Import all database models
# ============================================================
# These imports ensure every SQLAlchemy model is registered
# with Base.metadata before Alembic runs autogenerate.
# ============================================================

from app.db.models.user import User  # noqa: F401
from app.db.models.role import Role  # noqa: F401
from app.db.models.refresh_token import RefreshToken  # noqa: F401

from app.db.models.temple import Temple  # noqa: F401
from app.db.models.category import Category  # noqa: F401
from app.db.models.priest import Priest  # noqa: F401
from app.db.models.pooja import Pooja  # noqa: F401

from app.db.models.booking import Booking  # noqa: F401
from app.db.models.payment import Payment  # noqa: F401
from app.db.models.invoice import Invoice  # noqa: F401

from app.db.models.gallery import Gallery  # noqa: F401
from app.db.models.notification import Notification  # noqa: F401
from app.db.models.review import Review  # noqa: F401
from app.db.models.contact import Contact  # noqa: F401

from app.db.models.catering import Catering  # noqa: F401
from app.db.models.kundli import Kundli  # noqa: F401
from app.db.models.consultation import Consultation  # noqa: F401

from app.db.models.chat_conversation import ChatConversation  # noqa: F401
from app.db.models.chat_message import ChatMessage  # noqa: F401


# ============================================================
# Alembic Configuration
# ============================================================

config = context.config


# ============================================================
# Database URL
# ============================================================
# Escape % characters for ConfigParser.
# This is required when DATABASE_URL contains URL-encoded
# characters, especially in database passwords.
# ============================================================

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("%", "%%"),
)


# ============================================================
# Logging Configuration
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# Target Metadata
# ============================================================
# Alembic uses this metadata to detect:
# - New tables
# - Removed tables
# - New columns
# - Modified column types
# - Foreign keys
# - Indexes
# - Constraints
# ============================================================

target_metadata = Base.metadata


# ============================================================
# Offline Migration Mode
# ============================================================

def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.

    This configures Alembic with only the database URL
    without creating an actual database connection.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migration Mode
# ============================================================

def run_migrations_online() -> None:
    """
    Run migrations in online mode.

    This creates a database connection and executes
    migrations directly against the configured database.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Run Alembic
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()