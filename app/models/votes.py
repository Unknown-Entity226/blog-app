from __future__ import annotations

from ..database import Base
from sqlalchemy import UUID, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .posts import Post
    from .users import User


class Vote(Base):

    __tablename__ = "votes" 

    post_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('posts.id'), primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)

    vote_type: Mapped[int] = mapped_column(Integer, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="votes")
    user: Mapped["User"] = relationship("User", back_populates="votes")

    __table_args__=(
        CheckConstraint(
            "vote_type in (-1,1)", name = "check_vote_type"
        ),
    )