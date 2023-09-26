from fastapi import APIRouter
from .get_number import router as get_number_router

router = APIRouter(prefix="/luckydraw", tags=["luckydraw"])

router.include_router(get_number_router)
