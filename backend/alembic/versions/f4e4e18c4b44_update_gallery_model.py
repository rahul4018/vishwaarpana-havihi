"""Update gallery model

Revision ID: f4e4e18c4b44
Revises: 757adf3d0934
Create Date: 2026-07-22 16:50:45.662212

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4e4e18c4b44"
down_revision: Union[str, Sequence[str], None] = "757adf3d0934"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add new columns
    op.add_column(
        "gallery",
        sa.Column("image_url", sa.String(length=500), nullable=True),
    )

    op.add_column(
        "gallery",
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
    )

    op.add_column(
        "gallery",
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
    )

    # Copy existing media_url values into image_url
    op.execute(
        """
        UPDATE gallery
        SET image_url = media_url
        WHERE media_url IS NOT NULL
        """
    )

    # Make image_url NOT NULL after data migration
    op.alter_column(
        "gallery",
        "image_url",
        nullable=False,
    )

    # Remove old columns
    op.drop_column("gallery", "media_type")
    op.drop_column("gallery", "media_url")


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        "gallery",
        sa.Column("media_url", sa.String(length=500), nullable=False),
    )

    op.add_column(
        "gallery",
        sa.Column(
            "media_type",
            sa.String(length=30),
            server_default="IMAGE",
            nullable=False,
        ),
    )

    op.execute(
        """
        UPDATE gallery
        SET media_url = image_url
        WHERE image_url IS NOT NULL
        """
    )

    op.drop_column("gallery", "is_active")
    op.drop_column("gallery", "display_order")
    op.drop_column("gallery", "image_url")