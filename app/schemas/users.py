from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str

class UserResponse(BaseModel):
    username: str
    updated_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str]= None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    
    