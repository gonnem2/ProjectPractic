from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Annotated
from sqlalchemy import update, select

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.routers.auth.utils import get_current_user
from src.models.user import User

router = APIRouter(prefix="/premission", tags=["Premission"])


@router.patch("/set/{user_id}", status_code=status.HTTP_200_OK)
async def set_permission(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[int, Path()],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not current_user.get("is_team_lead"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission"
        )
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user.is_hr:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_hr=False, is_team_lead=True)
        )
        await db.commit()
        return status.HTTP_200_OK
    if user.is_team_lead:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_hr=True, is_team_lead=False)
        )
        await db.commit()
        return status.HTTP_200_OK
