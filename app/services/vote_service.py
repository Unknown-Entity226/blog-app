from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.users import User
from ..schemas.users import UserCreate, UserUpdate
from ..utils.security import hash_pass


