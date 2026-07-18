"""Rework planes into UAV maintenance/operating-time tracking domain

Revision ID: ac9f38563f26
Revises: 79b604fe4913
Create Date: 2026-07-18 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ac9f38563f26"
down_revision: Union[str, Sequence[str], None] = "79b604fe4913"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("planes", "uavs")

    op.alter_column("uavs", "type_plane", new_column_name="uav_model")
    op.alter_column("uavs", "belong_plane", new_column_name="operator")
    op.alter_column("uavs", "base_airfield", new_column_name="base_location")
    op.alter_column("uavs", "operating_time", new_column_name="total_operating_time")
    op.alter_column("uavs", "manufacturer_date", new_column_name="manufacture_date")
    op.alter_column(
        "uavs",
        "uav_model",
        type_=sa.String(length=50),
        existing_type=sa.String(length=10),
    )

    op.add_column(
        "uavs",
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
    )

    op.create_table(
        "maintenance_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("interval_hours", sa.Integer(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "operating_time_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uav_id", sa.Integer(), nullable=False),
        sa.Column("flight_date", sa.Date(), nullable=False),
        sa.Column("duration_hours", sa.Float(), nullable=False),
        sa.Column("cycles", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["uav_id"], ["uavs.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "maintenance_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uav_id", sa.Integer(), nullable=False),
        sa.Column("maintenance_type_id", sa.Integer(), nullable=True),
        sa.Column("performed_at", sa.Date(), nullable=False),
        sa.Column("operating_time_at_maintenance", sa.Integer(), nullable=False),
        sa.Column("performed_by", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("next_due_operating_time", sa.Integer(), nullable=True),
        sa.Column("next_due_date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["uav_id"], ["uavs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["maintenance_type_id"], ["maintenance_types.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("maintenance_records")
    op.drop_table("operating_time_logs")
    op.drop_table("maintenance_types")

    op.drop_column("uavs", "status")

    op.alter_column(
        "uavs",
        "uav_model",
        type_=sa.String(length=10),
        existing_type=sa.String(length=50),
    )
    op.alter_column("uavs", "manufacture_date", new_column_name="manufacturer_date")
    op.alter_column("uavs", "total_operating_time", new_column_name="operating_time")
    op.alter_column("uavs", "base_location", new_column_name="base_airfield")
    op.alter_column("uavs", "operator", new_column_name="belong_plane")
    op.alter_column("uavs", "uav_model", new_column_name="type_plane")

    op.rename_table("uavs", "planes")
