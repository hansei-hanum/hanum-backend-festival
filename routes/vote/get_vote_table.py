from datetime import datetime
from database import scope, VoteTable
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends
from depends.requireauth import RequireAuth

router = APIRouter()


@router.get("/primary")
async def get_primary_vote_table(user_id: int = Depends(RequireAuth)):
    async with scope() as session:
        table: VoteTable = (
            await session.execute(
                select(VoteTable)
                .where(
                    and_(
                        VoteTable.active == True,
                        VoteTable.start_at <= datetime.now(),
                        VoteTable.end_at >= datetime.now(),
                    )
                )
                .order_by(VoteTable.end_at.asc())
                .limit(1)
            )
        ).scalar_one_or_none()

        if table is None:
            return {
                "message": "VOTE_TABLE_NOT_FOUND",
                "data": None,
            }

        return {
            "message": "VOTE_TABLE_FOUND",
            "data": {
                "id": table.id,
                "title": table.title,
                "startAt": table.start_at,
                "endAt": table.end_at,
            },
        }
