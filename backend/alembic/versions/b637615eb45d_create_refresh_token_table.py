"""create_refresh_token_table

Revision ID: b637615eb45d
Revises: 3312fde260b3
Create Date: 2026-07-16 12:00:57.220440

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b637615eb45d"
down_revision: Union[str, Sequence[str], None] = "3312fde260b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "refresh_token",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("jti", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_refresh_token_jti"),
        "refresh_token",
        ["jti"],
        unique=True,
    )

    op.create_index(
        op.f("ix_refresh_token_user_id"),
        "refresh_token",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_refresh_token_expires_at",
        "refresh_token",
        ["expires_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_refresh_token_expires_at",
        table_name="refresh_token",
    )

    op.drop_index(
        op.f("ix_refresh_token_user_id"),
        table_name="refresh_token",
    )

    op.drop_index(
        op.f("ix_refresh_token_jti"),
        table_name="refresh_token",
    )

    op.drop_table("refresh_token")