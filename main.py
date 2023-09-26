import os
from fastapi import FastAPI
from routes import include_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from database import engine, Base

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"message": exc.detail, "data": None}, status_code=exc.status_code)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as sess:
        await sess.run_sync(Base.metadata.create_all)


include_router(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=os.environ["HOST"], port=int(os.environ["PORT"]), reload=True)
