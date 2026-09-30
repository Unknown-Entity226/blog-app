from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from ..models.posts import Post
from ..models.votes import Vote
from ..schemas.votes import VoteCreate


def vote_create(db: Session, vote: VoteCreate, post_id: UUID, user_id: UUID):
    post = db.scalar(select(Post).where(Post.id == post_id))

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    existing_vote = db.scalar(
        select(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)
    )
    if existing_vote is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already voted on this post",
        )

    new_vote = Vote(
        post_id=post_id,
        user_id=user_id,
        vote_type=int(vote.vote_type),
    )

    post.rating += int(vote.vote_type)

    db.add(new_vote)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already voted on this post",
        )

    db.refresh(new_vote)
    db.refresh(post)

    return new_vote


