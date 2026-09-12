from fastapi import APIRouter, Query, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..services.user_service import create_user, get_users, delete_user, update_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user: UserCreate, db: SessionDep):
    return create_user(db, user)


@router.get(path="", response_model=list[UserResponse])
def get_users_by_username(
    db: SessionDep,
    username: str = Query(description="Filter users by username"),
):
    return get_users(db, username)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: UUID, db: SessionDep):
    delete_user(db, id)


@router.put(path="/{id}", response_model=UserResponse)
def update(id: UUID, user: UserUpdate, db: SessionDep):
    return update_user(db, id, user)
