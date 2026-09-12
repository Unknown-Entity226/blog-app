from fastapi import APIRouter, Query, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.posts import PostCreate, PostResponse, UpdatePost
from ..services.post_service import create_post, delete_post, get_posts, update_post

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post(path="", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create(post: PostCreate, db: SessionDep):

    return create_post(db, post)


@router.get(path="")
def getPost(title: str = Query(description="Enter the post title"), db: SessionDep = None):
    return get_posts(db, title)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: UUID, db: SessionDep):
    delete_post(db, id)


@router.put(path="/{id}", response_model=PostResponse)
def updatePost(id: UUID, post: UpdatePost, db: SessionDep):
    return update_post(db, id, post)
