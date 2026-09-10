from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import Depends
from typing import Annotated

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class Base(DeclarativeBase):
    pass

