from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from ..database import SessionDep
from ..schemas.votes import VoteCreate, VoteResponse
from ..services.vote_service import delete_vote, update_vote, vote_create
from ..utils.outh2 import get_current_user
from ..schemas.auth import TokenData

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)


def get_current_user_id(current_user: TokenData) -> UUID:
    try:
        return UUID(str(current_user.id))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate the user",
        )


@router.post(path="/{post_id}", status_code=status.HTTP_201_CREATED, response_model=VoteResponse)
def vote(post_id: UUID, vote: VoteCreate, db: SessionDep, current_user: TokenData = Depends(get_current_user),
):
    return vote_create(db, vote, post_id, get_current_user_id(current_user))


@router.put(path="/{post_id}", response_model=VoteResponse)
def update_vote_by_id(
    post_id: UUID,
    vote: VoteCreate,
    db: SessionDep,
    current_user: TokenData = Depends(get_current_user),
):
    return update_vote(db, vote, post_id, get_current_user_id(current_user))


@router.delete(path="/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vote_by_id(
    post_id: UUID,
    db: SessionDep,
    current_user: TokenData = Depends(get_current_user),
):
    delete_vote(db, post_id, get_current_user_id(current_user))


