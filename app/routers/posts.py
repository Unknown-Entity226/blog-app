from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.posts import PostCreate, PostListResponse, PostResponse, UpdatePost
from ..services.post_service import create_post, delete_post, get_posts, update_post
from ..utils.outh2 import get_current_user
from ..schemas.auth import TokenData

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def get_current_user_id(current_user: TokenData) -> UUID:
    """Convert the authenticated token subject into the model's UUID type."""
    try:
        return UUID(str(current_user.id))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate the user",
        )


@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create(
    post: PostCreate,
    db: SessionDep,
    current_user: TokenData = Depends(get_current_user),
):
    return create_post(db, post, get_current_user_id(current_user))


@router.get(path="", response_model=PostListResponse)
def get_post(
    db: SessionDep,
    title: str = Query(description="Enter the post title"),
):
    return get_posts(db, title)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(
    id: UUID,
    db: SessionDep,
    current_user: TokenData = Depends(get_current_user),
):
    delete_post(db, id, get_current_user_id(current_user))


@router.put(path="/{id}", response_model=PostResponse)
def update_post_by_id(
    id: UUID,
    post: UpdatePost,
    db: SessionDep,
    current_user: TokenData = Depends(get_current_user),
):
    return update_post(db, id, post, get_current_user_id(current_user))
