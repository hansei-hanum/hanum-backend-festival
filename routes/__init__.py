from fastapi import FastAPI
from .timetable import router as timetable_router
from .schedule import router as schedule_router


def include_router(app: FastAPI):
    app.include_router(timetable_router)
    app.include_router(schedule_router)
