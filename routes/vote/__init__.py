from fastapi import APIRouter
from .get_vote_table import router as get_vote_table_router

router = APIRouter(prefix="/vote", tags=["vote"])

router.include_router(get_vote_table_router)
