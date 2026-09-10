from pydantic import BaseModel
from uuid import UUID
from datetime import date, time
from typing import Optional

class PostCreate(BaseModel):
    post_title: str
    post_content: str


class PostResponse(BaseModel):
    id: UUID
    post_title: str
    post_content: str
    post_date: date
    post_time: time
    rating: int

class UpdatePost(BaseModel):
    post_title: Optional[str] = None
    post_content: Optional[str] = None