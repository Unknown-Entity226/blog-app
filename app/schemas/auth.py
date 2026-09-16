from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserSignUp(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password:str