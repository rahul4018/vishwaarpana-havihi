"""create priest availability table

Revision ID: 757adf3d0934
Revises: 8f1dc71bec4f
Create Date: 2026-07-21 18:03:52.259826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "757adf3d0934"
down_revision: Union[str, Sequence[str], None] = "8f1dc71bec4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "priest_availability",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "priest_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "available_date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "start_time",
            sa.Time(),
            nullable=False,
        ),
        sa.Column(
            "end_time",
            sa.Time(),
            nullable=False,
        ),
        sa.Column(
            "is_available",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "remarks",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["priest_id"],
            ["priest.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_priest_availability_priest_id",
        "priest_availability",
        ["priest_id"],
    )

    op.create_index(
        "ix_priest_availability_available_date",
        "priest_availability",
        ["available_date"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_priest_availability_available_date",
        table_name="priest_availability",
    )

    op.drop_index(
        "ix_priest_availability_priest_id",
        table_name="priest_availability",
    )

    op.drop_table("priest_availability")