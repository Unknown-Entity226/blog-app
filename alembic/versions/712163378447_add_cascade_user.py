"""add cascade user

Revision ID: 712163378447
Revises: 086612f84570
Create Date: 2026-09-29 17:02:29.599153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '712163378447'
down_revision: Union[str, Sequence[str], None] = '086612f84570'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
