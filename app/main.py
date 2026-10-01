from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.posts import router as posts_router
from .routers.users import router as users_router
from .routers.auth import router as auth_router
from .routers.votes import router as vote_router


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins 
    allow_credentials=True,# Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(vote_router)

@app.get(path="/")
def home()->dict:
    return ({"message": "you are at index"})
