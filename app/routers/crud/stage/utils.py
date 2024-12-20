from typing import Annotated
from fastapi import Depends, status, HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.stage import Stage
from app.routers.auth.utils import get_current_user


async def check_premission(
    current_user: dict,
):
    if not current_user.get("is_team_lead"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission!"
        )


async def check_is_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: str,
):

    stage_from_db = await db.scalar(select(Stage).where(Stage.name == name))
    if stage_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stage is not DB!"
        )


async def check_is_not_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: str,
):

    stage_from_db = await db.scalar(select(Stage).where(Stage.name == name))
    if stage_from_db is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Stage already in db!"
        )
