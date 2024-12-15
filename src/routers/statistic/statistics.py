from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.statistic import Statistic
from src.routers.auth.utils import get_current_user

router = APIRouter(tags=["Statistic"], prefix="/statistic")


@router.get("/", summary="Возвращает всю статистику")
async def say_hello(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    statistic = (await db.scalars(select(Statistic))).all()

    if len(statistic) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Statistic service is unvailable",
        )

    return statistic
