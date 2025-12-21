"""add nullable for manufacturer_date - table planes

Revision ID: 79b604fe4913
Revises: 27d811817dc4
Create Date: 2025-12-21 19:23:38.044222

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79b604fe4913"
down_revision: Union[str, Sequence[str], None] = "27d811817dc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        table_name='planes',
        column_name='manufacturer_date',
        existing_type=sa.Date(),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        table_name='planes',
        column_name='manufacturer_date',
        existing_type=sa.Date(),
        nullable=False
    )
