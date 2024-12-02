from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.routers.auth.utils import get_current_user
from src.models.stage import Stage
from .utils import check_is_stage, check_is_not_stage, check_premission

router = APIRouter(prefix="/crud_stage", tags=["Stage"])


@router.get("/", summary="👀 Показать все стадии")
async def get_stages(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    stages = await db.scalars(select(Stage))
    return stages.all()


@router.post("/", summary="🚧 Создать стадию")
async def create_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    name: str,
):
    await check_premission(current_user)
    await check_is_not_stage(db=db, name=name)
    db.add(Stage(name=name))
    await db.commit()

    return {"Success": True}


@router.put("/", summary="🔄 Обновить стадию")
async def put_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    old_name: str,
    new_name: str,
):
    await check_premission(current_user)
    await check_is_not_stage(db=db, name=new_name)

    await db.execute(update(Stage).where(Stage.name == old_name).values(name=new_name))
    await db.commit()

    return {"Success": True}


@router.delete("/", status_code=status.HTTP_200_OK, summary="❌ Удалить стадию")
async def delete_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    name: str,
):
    await check_premission(current_user)
    await check_is_stage(db=db, name=name)
    await db.execute(delete(Stage).where(Stage.name == name))
    await db.commit()

    return {"message": "Stage has been deleted"}
