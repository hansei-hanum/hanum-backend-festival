from fastapi import APIRouter, Depends
from depends import RequireAuth
from pydantic import BaseModel

router = APIRouter()


class GetLuckyNumberRequest(BaseModel):
    token: str


@router.post("/lucky_numbers")
async def get_lucky_number(userid=Depends(RequireAuth)):
    return {"message": "SUCCESS", "data": 7}
