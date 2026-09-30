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

    if int(vote.vote_type) > 0:
        post.upvotes += 1
    else:
        post.downvotes += 1

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


def update_vote(db: Session, vote: VoteCreate, post_id: UUID, user_id: UUID):
    post = db.scalar(select(Post).where(Post.id == post_id))

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    existing_vote = db.scalar(
        select(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)
    )
    if existing_vote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has not voted on this post",
        )

    new_vote_value = int(vote.vote_type)
    old_vote_value = int(existing_vote.vote_type)

    if old_vote_value > 0:
        post.upvotes -= 1
    else:
        post.downvotes -= 1

    if new_vote_value > 0:
        post.upvotes += 1
    else:
        post.downvotes += 1

    existing_vote.vote_type = new_vote_value

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not update vote",
        )

    db.refresh(existing_vote)
    db.refresh(post)

    return existing_vote


def delete_vote(db: Session, post_id: UUID, user_id: UUID):
    post = db.scalar(select(Post).where(Post.id == post_id))

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    existing_vote = db.scalar(
        select(Vote).where(Vote.post_id == post_id, Vote.user_id == user_id)
    )
    if existing_vote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has not voted on this post",
        )

    if int(existing_vote.vote_type) > 0:
        post.upvotes -= 1
    else:
        post.downvotes -= 1

    db.delete(existing_vote)
    db.commit()
    db.refresh(post)

    return None


