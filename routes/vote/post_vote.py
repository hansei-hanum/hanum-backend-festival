from datetime import datetime
import logging

from pydantic import BaseModel, Field
from database import scope, VoteTable
from sqlalchemy import and_, exists, func, select
from fastapi import APIRouter, Depends
from database.vote import Vote, VoteField
from depends.requireauth import RequireAuth

router = APIRouter()


class PostVoteRequest(BaseModel):
    field_id: int = Field(..., alias="fieldId")


@router.post("/{vote_table_id}")
async def post_vote(
    request: PostVoteRequest,
    vote_table_id: int,
    user_id: int = Depends(RequireAuth),
):
    async with scope() as session:
        if not (
            await session.execute(
                select(VoteTable).where(
                    and_(
                        VoteTable.id == vote_table_id,
                        VoteTable.active == True,
                        VoteTable.start_at <= datetime.now(),
                        VoteTable.end_at >= datetime.now(),
                    )
                )
            )
        ).scalar_one_or_none():
            return {
                "message": "VOTE_TABLE_NOT_FOUND",
                "data": None,
            }

        if not (
            await session.execute(
                select(VoteField).where(
                    and_(
                        VoteField.id == request.field_id,
                        VoteField.vote_table_id == vote_table_id,
                    )
                )
            )
        ).scalar_one_or_none():
            return {
                "message": "VOTE_FIELD_NOT_FOUND",
                "data": None,
            }

        if (
            await session.execute(
                select(Vote).where(
                    and_(
                        Vote.user_id == user_id,
                        Vote.vote_table_id == vote_table_id,
                    )
                )
            )
        ).scalar_one_or_none():
            return {
                "message": "ALREADY_VOTED",
                "data": None,
            }

        vote = Vote(
            user_id=user_id,
            vote_table_id=vote_table_id,
            vote_field_id=request.field_id,
        )

        session.add(vote)
        await session.commit()

        return {
            "message": "SUCCESS",
            "data": {
                "total": await Vote.total(session, vote_table_id),
            },
        }
