from pydantic import BaseModel
from typing import Optional

class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

# for login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    