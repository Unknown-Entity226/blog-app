from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.users import User
from ..schemas.users import UserCreate, UserUpdate
from ..utils.security import hash_pass

def create_user(db: Session, user: UserCreate):

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


def get_users(db: Session, username: str):
    statement = select(User).where(User.username.ilike(f"%{username}%"))
    results = db.scalars(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
    return results


def delete_user(db: Session, id: UUID):
    statement = select(User).where(User.id == id)
    result = db.scalar(statement)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id} found")

    db.delete(result)
    db.commit()


def update_user(db: Session, id: UUID, user: UserUpdate):
    statement = select(User).where(User.id == id)
    existing = db.scalar(statement)

    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id: {id} found")

    updated = user.model_dump(exclude_unset=True)
    password = updated.pop("password", None)
    if password is not None:
        updated["password_hash"] = hash_pass(password)

    for key, val in updated.items():
        setattr(existing, key, val)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists",
        )
    db.refresh(existing)

    return existing
