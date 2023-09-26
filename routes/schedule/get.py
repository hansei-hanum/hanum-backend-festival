from fastapi import APIRouter, Depends
from depends import RequireAuth
from neis import TimeTable
from fastapi import HTTPException
from micro import auth
from neis import Schedule

router = APIRouter()


@router.get("/{month}")
async def get_schedule_calender(month: int, userid: int = Depends(RequireAuth)):
    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    schedule = await Schedule.get(month)

    return {"message": "SUCCESS", "data": schedule}


@router.get("/")
async def get_schedule(userid: int = Depends(RequireAuth)):
    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    schedule = await Schedule.get()

    return {"message": "SUCCESS", "data": schedule}
