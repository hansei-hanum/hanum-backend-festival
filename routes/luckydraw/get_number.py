from fastapi import APIRouter, Depends
from depends import RequireAuth
from pydantic import BaseModel
from database import LuckyNumber, LuckyToken

router = APIRouter()


class GetLuckyNumberRequest(BaseModel):
    token: str


@router.post("/lucky_numbers")
async def get_lucky_number(userid=Depends(RequireAuth)):
    pass
