from fastapi import APIRouter, Query, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.users import UserCreate, UserResponse, UserUpdate
from ..services.post_service import create_post, delete_post, get_posts, update_post

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

