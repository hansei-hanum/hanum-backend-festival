from fastapi import FastAPI
from .luckydraw import router as luckydraw_router
from .vote import router as vote_router


def include_router(app: FastAPI):
    app.include_router(luckydraw_router)
    app.include_router(vote_router)
