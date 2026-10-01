from fastapi import APIRouter, HTTPException, Query, status, Depends
from uuid import UUID
from ..database import SessionDep
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..schemas.auth import TokenData
from ..services.user_service import create_user, get_users, delete_user, update_user
from ..utils.outh2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user_id(current_user: TokenData) -> UUID:
    """Convert the authenticated token subject into the model's UUID type."""
    try:
        return UUID(str(current_user.id))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate the user",
        )

@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user: UserCreate, db: SessionDep):
    return create_user(db, user)


@router.get(path="", response_model=list[UserResponse])
def get_users_by_username(
    db: SessionDep,
    username: str = Query(description="Filter users by username"),
):
    return get_users(db, username)


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
def delete(db: SessionDep, current_user: TokenData = Depends(get_current_user)):
    delete_user(db, id = get_current_user_id(current_user))


@router.put(path="/", response_model=UserResponse)
def update(user: UserUpdate, db: SessionDep, current_user: TokenData = Depends(get_current_user)):
    return update_user(db= db,id = get_current_user_id(current_user), user = user)
