from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.stage import Stage
from src.routers.auth.utils import get_current_user
from src.schemas.request.create_sla_settings import CreateSLA
from src.models.sla_settings import SLASettings
from src.schemas.response.response import Response

router = APIRouter(
    prefix="/sla",
    tags=["SLA AND VIOLATIONS"],
)


@router.post(
    "/settings",
    summary="Задать настройку sla-таблицы (max время в стадии)",
    status_code=status.HTTP_201_CREATED,
)
async def create_sla_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    sla_settings_from_user: CreateSLA,
):
    if not current_user.get("is_team_lead"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission!"
        )

    sla_from_bd = await db.scalar(
        select(SLASettings).where(
            SLASettings.stage_id == sla_settings_from_user.stage_id
        )
    )

    if sla_from_bd is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="SLA settings already in db"
        )

    max_stage = await db.scalar(select(func.max(Stage.id)))

    if max_stage < sla_settings_from_user.stage_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Stage with this id not found"
        )

    sla_for_db = SLASettings(
        stage_id=sla_settings_from_user.stage_id,
        max_time=sla_settings_from_user.max_time,
    )
    db.add(sla_for_db)
    await db.commit()

    return Response(status=status.HTTP_201_CREATED, message="sla_setting created")


@router.get("/settings", summary="Вернуть все настройки стадий")
async def get_all_sla_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    return (await db.scalars(select(SLASettings))).all()
