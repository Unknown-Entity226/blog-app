from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.posts import Post
from ..schemas.posts import PostCreate, UpdatePost


def create_post(db: Session, post: PostCreate, user_id: UUID):
    new_post = Post(**post.model_dump(), user_id=user_id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_posts(db: Session, title: str):
    statement = select(Post).where(
        Post.post_title.ilike(f"%{title}%"),
    )
    results = db.scalars(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    return {"data": results}


def delete_post(db: Session, id: UUID, user_id: UUID):
    statement = select(Post).where(Post.id == id, Post.user_id == user_id)
    result = db.scalar(statement)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found")

    db.delete(result)
    db.commit()


def update_post(db: Session, id: UUID, post: UpdatePost, user_id: UUID):
    statement = select(Post).where(Post.id == id, Post.user_id == user_id)
    existing = db.scalar(statement)

    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found")

    updated = post.model_dump(exclude_unset=True)
    for key, val in updated.items():
        setattr(existing, key, val)

    db.commit()
    db.refresh(existing)

    return existing
