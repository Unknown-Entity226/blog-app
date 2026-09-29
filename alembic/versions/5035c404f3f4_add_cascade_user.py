"""add cascade user

Revision ID: 5035c404f3f4
Revises: 712163378447
Create Date: 2026-09-29 17:05:01.056306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5035c404f3f4'
down_revision: Union[str, Sequence[str], None] = '712163378447'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
