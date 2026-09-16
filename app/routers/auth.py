from fastapi import APIRouter, Query, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.auth import UserSignUp, UserLogin

router = APIRouter(prefix="/auth", tags=["Authetication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignUp, db: SessionDep):
    return create_user()


@router.post(path="/login", status_code=status.HTTP_202_ACCEPTED)
def login(user: UserLogin, db:SessionDep):
    return 