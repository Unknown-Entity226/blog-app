from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database import SessionDep
from ..schemas.auth import TokenResponse, UserSignUp
from ..schemas.users import UserResponse
from ..services.auth_service import login_user, signup_user


router = APIRouter(prefix="/auth", tags=["Authetication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup(user: UserSignUp, db: SessionDep):
    return signup_user(db, user)


@router.post(path="/login", response_model=TokenResponse)
def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
):
    return login_user(db, credentials)
