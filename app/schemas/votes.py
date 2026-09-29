from pydantic import BaseModel, ConfigDict, Field, AliasPath

class VoteResponse(BaseModel):
    post_title: str = Field(validation_alias=AliasPath("post", "post_title"))
    vote_type: int

    model_config = ConfigDict(from_attributes=True)
