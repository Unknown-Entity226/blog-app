from fastapi import APIRouter, Query, status
from uuid import UUID
from ..database import SessionDep


router = APIRouter(
    prefix="/votes", 
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote():
    