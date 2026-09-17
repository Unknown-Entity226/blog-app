from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..models.users import User
from ..schemas.auth import UserSignUp
from ..utils.security import hash_pass, verify_pass
from ..utils.outh2 import create_access_token


def get_user_by_username(db: Session, username: str):
    statement = select(User).where(User.username == username)

    return db.scalar(statement)


def signup_user(db: Session, user: UserSignUp):

    user_data = user.model_dump()

    password = user_data.pop("password")

    user_data["password_hash"] = hash_pass(password)

    new_user = User(**user_data)

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists",
        )

    db.refresh(new_user)

    return new_user


def login_user(db: Session, credentials: OAuth2PasswordRequestForm):
    actual = get_user_by_username(db, credentials.username)

    if actual is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    if not verify_pass(
        credentials.password,
        actual.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    access_token = create_access_token(data = {"sub": str(actual.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
