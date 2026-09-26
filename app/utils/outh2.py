from datetime import timedelta, datetime, timezone
from uuid import UUID
import os

from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

from sqlalchemy import select

from ..schemas.auth import TokenData
from ..database import SessionDep
from ..models.users import User

load_dotenv()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("sub")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(db: SessionDep, token: str = Depends(oauth2_schema)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate the user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    statement = select(User).where(User.id == UUID(token_data.id))

    result = db.scalar(statement)

    if result is None:
        raise credentials_exception

    return result
