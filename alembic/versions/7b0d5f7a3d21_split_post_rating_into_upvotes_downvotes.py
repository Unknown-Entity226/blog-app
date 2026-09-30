"""split post rating into upvotes and downvotes

Revision ID: 7b0d5f7a3d21
Revises: c84f5d9e2a10
Create Date: 2026-09-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b0d5f7a3d21"
down_revision: Union[str, Sequence[str], None] = "c84f5d9e2a10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add separate upvote/downvote counters and backfill from the votes table."""
    op.add_column("posts", sa.Column("upvotes", sa.Integer(), nullable=True, server_default="0"))
    op.add_column("posts", sa.Column("downvotes", sa.Integer(), nullable=True, server_default="0"))

    op.execute(
        """
        UPDATE posts
        SET upvotes = (
            SELECT COUNT(*)
            FROM votes
            WHERE votes.post_id = posts.id AND votes.vote_type = 1
        ),
            downvotes = (
            SELECT COUNT(*)
            FROM votes
            WHERE votes.post_id = posts.id AND votes.vote_type = -1
        )
        """
    )

    op.alter_column("posts", "upvotes", nullable=False, server_default="0")
    op.alter_column("posts", "downvotes", nullable=False, server_default="0")

    op.drop_column("posts", "rating")


def downgrade() -> None:
    """Restore the single rating field from the derived vote totals."""
    op.add_column("posts", sa.Column("rating", sa.Integer(), nullable=True, server_default="0"))

    op.execute(
        """
        UPDATE posts
        SET rating = upvotes - downvotes
        """
    )

    op.alter_column("posts", "rating", nullable=False, server_default="0")
    op.drop_column("posts", "upvotes")
    op.drop_column("posts", "downvotes")
