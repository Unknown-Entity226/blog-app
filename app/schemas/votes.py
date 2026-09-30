from pydantic import BaseModel, ConfigDict, Field, AliasPath
import uuid
from enum import IntEnum

class VoteType(IntEnum):

    UPVOTE = 1
    DOWNVOTE = -1

class VoteCreate(BaseModel):

    vote_type: VoteType

class VoteResponse(BaseModel):
    post_title: str = Field(validation_alias=AliasPath("post", "post_title"))
    vote_type: VoteType

    model_config = ConfigDict(from_attributes=True)
