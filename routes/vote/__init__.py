from fastapi import APIRouter
from .get_vote import router as get_vote_router
from .post_vote import router as post_vote_router

router = APIRouter(prefix="/vote", tags=["vote"])

router.include_router(get_vote_router)
router.include_router(post_vote_router)
