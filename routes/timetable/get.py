from fastapi import APIRouter, Depends
from depends import RequireAuth
from neis import TimeTable
from fastapi import HTTPException
from micro import auth

router = APIRouter()


@router.get("/")
async def get_timetable(userid: int = Depends(RequireAuth)):
    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    if not user.verification.type == "STUDENT":
        raise HTTPException(status_code=403, detail="USER_NOT_VERIFIED")

    timetable = await TimeTable.get(
        user.verification.department,
        user.verification.grade,
        user.verification.classroom,
    )

    return {"message": "SUCCESS", "data": timetable}
