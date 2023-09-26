from datetime import datetime
from database import scope, VoteTable
from sqlalchemy import and_, select
from fastapi import APIRouter, Depends
from database.vote import Vote, VoteField
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

        myVote: Vote | None = (
            await session.execute(
                select(Vote).where(
                    and_(
                        Vote.user_id == user_id,
                        Vote.vote_table_id == table.id,
                    )
                )
            )
        ).scalar_one_or_none()

        return {
            "message": "SUCCESS",
            "data": {
                "id": table.id,
                "title": table.title,
                "startAt": table.start_at,
                "endAt": table.end_at,
                "fields": [
                    {
                        "id": field.id,
                        "value": field.value,
                    }
                    for field in (
                        await session.execute(
                            select(VoteField).where(VoteField.vote_table_id == table.id)
                        )
                    ).scalars()
                ],
                "myVote": {
                    "id": myVote.id,
                    "fieldId": myVote.vote_field_id,
                    "createdAt": myVote.created_at,
                },
                "total": await Vote.total(session, table.id),
            },
        }
