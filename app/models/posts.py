from ..database import Base
from sqlalchemy import Integer, String, Date, Time, Text, UUID, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, time
import uuid

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)

    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    post_title: Mapped[str] = mapped_column(String, nullable=False)

    post_content: Mapped[str] = mapped_column(Text, nullable=False)

    post_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=text('CURRENT_DATE'))

    post_time: Mapped[time] = mapped_column(Time, nullable=False, server_default=text('CURRENT_TIME'))

    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
