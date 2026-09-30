"""created voter table

Revision ID: 40853cc930c8
Revises: df0f0c9bcbfd
Create Date: 2026-09-30 16:41:06.831757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40853cc930c8'
down_revision: Union[str, Sequence[str], None] = 'df0f0c9bcbfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
