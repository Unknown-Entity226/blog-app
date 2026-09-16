from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.users import User
from ..schemas.auth import UserSignUp, UserLogin
from ..utils.security import hash_pass, verify_pass


def get_user_by_email(db: Session, email: str):

    statement = select(User).where(User.email == email)

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


def login_user(db: Session, user: UserLogin):

    user_data = user.model_dump()

    actual = get_user_by_email(db, user_data["email"])

    if actual is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    if not verify_pass(
        user_data["password"],
        actual.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    return actual