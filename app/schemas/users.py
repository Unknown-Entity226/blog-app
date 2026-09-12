from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password_hash: str | None = None
    
