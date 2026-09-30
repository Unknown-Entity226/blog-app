from datetime import date, time
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models.posts import Post
from app.models.users import User
from app.models.votes import Vote
from app.schemas.votes import VoteCreate, VoteType
from app.services.vote_service import delete_vote, update_vote


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_update_vote_changes_rating():
    engine = setup_db()
    with Session(engine) as db:
        user = User(
            username="alice",
            email="alice@example.com",
            password_hash="hash",
        )
        db.add(user)
        db.flush()

        post = Post(
            id=uuid4(),
            user_id=user.id,
            post_title="Test",
            post_content="Hello",
            post_date=date.today(),
            post_time=time(12, 0),
            upvotes=1,
            downvotes=0,
        )
        db.add(post)
        db.flush()

        vote = Vote(post_id=post.id, user_id=user.id, vote_type=1)
        db.add(vote)
        db.commit()

        updated = update_vote(db, VoteCreate(vote_type=VoteType.DOWNVOTE), post.id, user.id)

        assert updated.vote_type == VoteType.DOWNVOTE
        assert post.upvotes == 0
        assert post.downvotes == 1
        assert post.rating == -1


def test_delete_vote_removes_vote_and_resets_rating():
    engine = setup_db()
    with Session(engine) as db:
        user = User(
            username="bob",
            email="bob@example.com",
            password_hash="hash",
        )
        db.add(user)
        db.flush()

        post = Post(
            id=uuid4(),
            user_id=user.id,
            post_title="Test",
            post_content="Hello",
            post_date=date.today(),
            post_time=time(12, 0),
            upvotes=1,
            downvotes=0,
        )
        db.add(post)
        db.flush()

        vote = Vote(post_id=post.id, user_id=user.id, vote_type=1)
        db.add(vote)
        db.commit()

        delete_vote(db, post.id, user.id)

        assert db.get(Vote, (post.id, user.id)) is None
        assert post.upvotes == 0
        assert post.downvotes == 0
        assert post.rating == 0
