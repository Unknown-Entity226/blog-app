from fastapi import FastAPI
from .database import engine
from .models import posts, users
from .routers.posts import router as posts_router
from .routers.users import router as users_router
from .routers.auth import router as auth_router


posts.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get(path="/")
def home()->dict:
    return ({"message": "you are at index"})
