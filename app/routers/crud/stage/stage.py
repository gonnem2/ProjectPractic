from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.routers.auth.utils import get_current_user
from app.models.stage import Stage
from .utils import check_is_stage, check_is_not_stage, check_premission
from app.schemas.response.stage_response import StageResponse
from app.schemas.response.all_stages import AllStageResponse
from app.schemas.response.response import Response

router = APIRouter(prefix="/crud_stage", tags=["Stage"])


@router.get(
    "/",
    summary="👀 Показать все стадии",
    response_model=AllStageResponse,
)
async def get_stages(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    stages = await db.scalars(select(Stage))
    return AllStageResponse(
        status=status.HTTP_200_OK,
        data=[StageResponse.from_orm(i) for i in stages.all()],
    )


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

    return Response(
        status=status.HTTP_201_CREATED,
        message="Stage created",
    )


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

    return Response(status=status.HTTP_201_CREATED, message="Stage's has been updated")


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

    return Response(status=status.HTTP_200_OK, message="Stage has been deleted")
