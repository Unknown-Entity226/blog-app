"""changes user and post model

Revision ID: df0f0c9bcbfd
Revises: e26a5ffe4973
Create Date: 2026-09-29 23:36:22.583502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df0f0c9bcbfd'
down_revision: Union[str, Sequence[str], None] = 'e26a5ffe4973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
