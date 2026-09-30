"""created voter table

Revision ID: a307070e4d66
Revises: 40853cc930c8
Create Date: 2026-09-30 16:46:12.220219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a307070e4d66'
down_revision: Union[str, Sequence[str], None] = '40853cc930c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # This revision was applied before it contained schema changes.
    # Keep it immutable; the next revision creates the missing table.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
