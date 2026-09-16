from fastapi import APIRouter, Query, status
from ..database import SessionDep
from ..schemas.auth import UserSignUp, UserLogin
from ..schemas.users import UserResponse
from ..services.auth_service import signup_user, login_user
router = APIRouter(prefix="/auth", tags=["Authetication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup(user: UserSignUp, db: SessionDep):
    return signup_user(db, user)


@router.post(path="/login", status_code=status.HTTP_202_ACCEPTED, response_model=UserResponse)
def login(user: UserLogin, db:SessionDep):
    return login_user(db, user)