from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.users import User
from ..schemas.auth import UserSignUp, UserLogin
from ..utils.security import hash_pass


def get_user_by_email(db: Session, email: str):

    statement = select(User).where(User.email.is_(f"{email}"))
    return db.scalar(statement)





    
