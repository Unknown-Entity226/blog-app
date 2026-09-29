from __future__ import annotations

from ..database import Base
from sqlalchemy import Integer, String, Date, Time, Text, UUID, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .users import User
    from .votes import Vote

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)

    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    post_title: Mapped[str] = mapped_column(String, nullable=False)

    post_content: Mapped[str] = mapped_column(Text, nullable=False)

    post_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=text('CURRENT_DATE'))

    post_time: Mapped[time] = mapped_column(Time, nullable=False, server_default=text('CURRENT_TIME'))

    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship("User", back_populates="posts")

    vote: Mapped[list["Vote"]] = relationship(back_populates="post", cascade="all, delete-orphan")
