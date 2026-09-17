from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.posts import Post
from ..schemas.posts import PostCreate, UpdatePost
from ..utils.outh2 import get_current_user

def create_post(db: Session, post: PostCreate, sub: str = Depends(get_current_user)):
    print(sub)
    new_post = Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_posts(db: Session, title: str, sub: str = Depends(get_current_user)):
    statement = select(Post).where(Post.post_title.ilike(f"%{title}%"))
    results = db.scalars(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    return {"data": results}


def delete_post(db: Session, id: UUID, sub: str = Depends(get_current_user)):
    statement = select(Post).where(Post.id == id)
    result = db.scalar(statement)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")

    db.delete(result)
    db.commit()


def update_post(db: Session, id: UUID, post: UpdatePost, sub: str = Depends(get_current_user)):
    statement = select(Post).where(Post.id == id)
    existing = db.scalar(statement)

    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")

    updated = post.model_dump(exclude_unset=True)
    for key, val in updated.items():
        setattr(existing, key, val)

    db.commit()
    db.refresh(existing)

    return existing
