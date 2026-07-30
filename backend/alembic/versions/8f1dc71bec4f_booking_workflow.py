"""booking workflow

Revision ID: 8f1dc71bec4f
Revises: 19fe601306ad
Create Date: 2026-07-20 17:56:03.973279
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "8f1dc71bec4f"
down_revision: Union[str, Sequence[str], None] = "19fe601306ad"
branch_labels = None
depends_on = None


booking_status_enum = postgresql.ENUM(
    "REQUESTED",
    "REVIEWING",
    "CUSTOMER_CONTACTED",
    "QUOTATION_PREPARING",
    "QUOTATION_SENT",
    "WAITING_FOR_CUSTOMER",
    "QUOTATION_ACCEPTED",
    "ADVANCE_PAYMENT_PENDING",
    "ADVANCE_PAID",
    "PAYMENT_VERIFIED",
    "PRIEST_ASSIGNED",
    "CATERING_ASSIGNED",
    "MATERIALS_READY",
    "CALENDAR_SHARED",
    "SERVICE_IN_PROGRESS",
    "SERVICE_COMPLETED",
    "FINAL_PAYMENT_PENDING",
    "COMPLETED",
    "CANCELLED",
    name="booking_status_enum",
    create_type=False,
)

quotation_status_enum = postgresql.ENUM(
    "DRAFT",
    "SENT",
    "VIEWED",
    "ACCEPTED",
    "REJECTED",
    "EXPIRED",
    "CANCELLED",
    name="quotation_status_enum",
    create_type=False,
)


def upgrade() -> None:

    bind = op.get_bind()

    booking_status_enum.create(bind, checkfirst=True)
    quotation_status_enum.create(bind, checkfirst=True)

    op.execute("""
        UPDATE booking
        SET booking_status='REQUESTED'
        WHERE booking_status='PENDING'
    """)

    op.execute("""
        UPDATE booking
        SET booking_status='COMPLETED'
        WHERE booking_status='CONFIRMED'
    """)

    op.create_table(
        "booking_quotation",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("booking_id", sa.UUID(), nullable=False),
        sa.Column("quotation_number", sa.String(30), nullable=False),
        sa.Column("priest_cost", sa.Numeric(10,2), nullable=False),
        sa.Column("material_cost", sa.Numeric(10,2), nullable=False),
        sa.Column("catering_cost", sa.Numeric(10,2), nullable=False),
        sa.Column("transport_cost", sa.Numeric(10,2), nullable=False),
        sa.Column("miscellaneous_cost", sa.Numeric(10,2), nullable=False),
        sa.Column("discount", sa.Numeric(10,2), nullable=False),
        sa.Column("tax", sa.Numeric(10,2), nullable=False),
        sa.Column("total_amount", sa.Numeric(10,2), nullable=False),
        sa.Column("advance_amount", sa.Numeric(10,2), nullable=False),
        sa.Column("remaining_amount", sa.Numeric(10,2), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("quotation_status", quotation_status_enum, nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True)),
        sa.Column("valid_until", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("quotation_number"),
    )

    op.create_index(
        "ix_booking_quotation_booking_id",
        "booking_quotation",
        ["booking_id"],
        unique=True,
    )

    op.create_table(
        "booking_status_history",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("booking_id", sa.UUID(), nullable=False),
        sa.Column("status", booking_status_enum, nullable=False),
        sa.Column("remarks", sa.Text()),
        sa.Column("updated_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"], ondelete="CASCADE"),
    )

    op.create_index(
        "ix_booking_status_history_booking_id",
        "booking_status_history",
        ["booking_id"],
    )

    op.create_table(
        "priest_assignment",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("booking_id", sa.UUID(), nullable=False),
        sa.Column("priest_id", sa.UUID(), nullable=False),
        sa.Column("assigned_by", sa.UUID(), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("is_confirmed", sa.Boolean(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["assigned_by"], ["user.id"]),
        sa.ForeignKeyConstraint(["booking_id"], ["booking.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["priest_id"], ["priest.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("booking_id"),
    )

    op.alter_column(
        "booking",
        "booking_status",
        existing_type=sa.String(30),
        type_=booking_status_enum,
        existing_nullable=False,
        postgresql_using="booking_status::booking_status_enum",
    )


def downgrade() -> None:

    op.alter_column(
        "booking",
        "booking_status",
        existing_type=booking_status_enum,
        type_=sa.String(30),
        existing_nullable=False,
        postgresql_using="booking_status::text",
    )

    op.drop_table("priest_assignment")
    op.drop_index("ix_booking_status_history_booking_id", table_name="booking_status_history")
    op.drop_table("booking_status_history")
    op.drop_index("ix_booking_quotation_booking_id", table_name="booking_quotation")
    op.drop_table("booking_quotation")

    quotation_status_enum.drop(op.get_bind(), checkfirst=True)
    booking_status_enum.drop(op.get_bind(), checkfirst=True)