from fastapi import APIRouter, Depends, HTTPException
from depends import RequireAuth
from pydantic import BaseModel
from micro import auth
from database import scope, LuckyNumber, LuckyToken
from sqlalchemy import select
from env import Env
from datetime import datetime, timezone
from pytz import timezone


router = APIRouter()


class GetLuckyNumberRequest(BaseModel):
    token: str


@router.post("/lucky_numbers")
async def get_lucky_number(request: GetLuckyNumberRequest, userid=Depends(RequireAuth)):
    if Env.NO_LUCKY_NUMBER_UNTIL:
        no_lucky_number_until = datetime.fromisoformat(Env.NO_LUCKY_NUMBER_UNTIL)

        if datetime.now(timezone("Asia/Seoul")) < no_lucky_number_until:
            raise HTTPException(403, "NOT_STARTED_YET")

    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(404, "USER_NOT_FOUND")

    if not user.verification.type in ["STUDENT", "TEACHER"]:
        raise HTTPException(403, "NOT_ALLOWED")

    async with scope() as session:
        existing_token = (
            await session.execute(
                select(LuckyToken).where(LuckyToken.user_id == userid)
            )
        ).scalar_one_or_none()

        if existing_token:
            raise HTTPException(409, "USER_ALREADY_HAS_LUCKY_NUMBER")

        token = (
            await session.execute(
                select(LuckyToken).where(LuckyToken.token == request.token)
            )
        ).scalar_one_or_none()

        if not token:
            raise HTTPException(404, "TOKEN_NOT_FOUND")

        if token.user_id:
            raise HTTPException(409, "TOKEN_ALREADY_USED")

        token.user_id = userid

        lucky_number = LuckyNumber(user_id=userid)
        session.add(lucky_number)
        await session.commit()
        await session.refresh(lucky_number)

        return {"message": "SUCCESS", "data": lucky_number.id}


@router.get("/lucky_number")
async def get_lucky_number(userid=Depends(RequireAuth)):
    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(404, "USER_NOT_FOUND")

    if not user.verification.type in ["STUDENT", "TEACHER"]:
        raise HTTPException(403, "NOT_ALLOWED")

    async with scope() as session:
        lucky_number = (
            await session.execute(
                select(LuckyNumber).where(LuckyNumber.user_id == userid)
            )
        ).scalar_one_or_none()

        if not lucky_number:
            raise HTTPException(404, "USER_HAS_NO_LUCKY_NUMBER")

        return {"message": "SUCCESS", "data": lucky_number.id}
