from pydantic import AliasPath, BaseModel, ConfigDict, Field
from datetime import date, time
from typing import Optional

class PostCreate(BaseModel):
    post_title: str
    post_content: str


class PostResponse(BaseModel):

    post_title: str
    post_content: str
    username: str = Field(validation_alias=AliasPath("user", "username"))
    post_date: date
    post_time: time
    upvotes: int
    downvotes: int
    rating: int

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    data: list[PostResponse]


class UpdatePost(BaseModel):
    post_title: Optional[str] = None
    post_content: Optional[str] = None

