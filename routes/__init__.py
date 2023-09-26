from fastapi import FastAPI
from .luckydraw import router as luckydraw_router


def include_router(app: FastAPI):
    app.include_router(luckydraw_router)
