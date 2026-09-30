"""create votes table

Revision ID: c84f5d9e2a10
Revises: a307070e4d66
Create Date: 2026-09-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c84f5d9e2a10"
down_revision: Union[str, Sequence[str], None] = "a307070e4d66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the votes table."""
    op.create_table(
        "votes",
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("vote_type", sa.Integer(), nullable=False),
        sa.CheckConstraint("vote_type IN (-1, 1)", name="check_vote_type"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("post_id", "user_id"),
    )


def downgrade() -> None:
    """Remove the votes table."""
    op.drop_table("votes")
