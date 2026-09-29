"""add cascade user

Revision ID: e26a5ffe4973
Revises: 5035c404f3f4
Create Date: 2026-09-29 17:07:01.096156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e26a5ffe4973'
down_revision: Union[str, Sequence[str], None] = '5035c404f3f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
