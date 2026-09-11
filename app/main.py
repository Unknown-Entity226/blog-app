from fastapi import FastAPI, Query, status, HTTPException
from pydantic import BaseModel, Field
from .database import engine, SessionDep
from .models import posts, users
from uuid import UUID
from sqlalchemy import select
from .schemas.posts import PostCreate, PostResponse, UpdatePost


posts.Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get(path="/")
def home()->dict:
    return ({"message": "you are at index"})

@app.post(path="/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db:SessionDep):
    new_post = posts.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get(path="/posts")
def getPost(title:str=Query(description="Enter the post title"), db: SessionDep = None):

    statement = select(posts.Post).where(posts.Post.post_title.ilike(f"%{title}%"))
    results = db.scalars(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    return {"data": results}


@app.delete(path="/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: UUID, db: SessionDep):

    statement = select(posts.Post).where(posts.Post.id == id)
    result = db.scalar(statement)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")

    db.delete(result)
    db.commit()


@app.put(path="/posts/{id}", response_model = PostResponse )
def updatePost(id:UUID, post:UpdatePost, db:SessionDep):

    statement = select(posts.Post).where(posts.Post.id == id)

    existing = db.scalar(statement)

    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {id} found")

    updated = post.model_dump(exclude_unset=True)
    print(updated)
    for key, val in updated.items():
        setattr(existing, key, val)

    db.commit()
    db.refresh(existing)

    return existing