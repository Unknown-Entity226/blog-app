from ..database import Base
from sqlalchemy import Integer, String, DateTime, UUID, text, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
