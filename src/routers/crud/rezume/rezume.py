from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from fastapi.params import Query
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.statistic import Statistic
from src.models.stage import Stage
from src.models.sla_settings import SLASettings
from src.models.rezume import Rezume
from src.routers.auth.utils import get_current_user
from src.schemas.request.rezume_scheme import CreateRezume
from src.schemas.response.response import Response
from src.schemas.response.all_rezumes import AllRezumeResponse
from src.schemas.response.rezume_response import RezumeResponse

router = APIRouter(prefix="/crud_rezume", tags=["Rezume"])


@router.post("/rezume")
async def create_rezume(
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume: CreateRezume,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not current_user.get("is_hr"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission"
        )
    rezume_from_db = await db.scalar(select(Rezume).where(Rezume.text == rezume.text))

    if rezume_from_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="rezume already in DB"
        )

    rezume_for_db = Rezume(
        vacancy_id=rezume.vacancy_id,
        source=rezume.source,
        text=rezume.text,
        user_id=current_user.get("id"),
    )
    time_for_stage = await db.scalar(
        select(SLASettings.max_time).where(SLASettings.stage_id == 6)
    )
    rezume_for_db.max_time = timedelta(seconds=int(time_for_stage)) + datetime.utcnow()
    db.add(rezume_for_db)
    await db.commit()

    return Response(status=status.HTTP_201_CREATED, message="rezume has been uploaded!")


@router.get("/rezume", response_model=AllRezumeResponse)
async def get_all_rezumes(db: Annotated[AsyncSession, Depends(get_db)]):
    rezumes = await db.scalars(select(Rezume))
    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes.all()],
    )


@router.put("/rezume/{rezume_id}", response_model=Response)
async def update_rezume(
    rezume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume: CreateRezume,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    rezume_from_db = await db.scalar(select(Rezume).where(Rezume.id == rezume_id))

    if rezume_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Rezume not found"
        )

    await db.execute(
        update(Rezume).values(
            vacancy_id=rezume.vacancy_id,
            source=rezume.source,
            text=rezume.text,
            user_id=current_user.get("id"),
        )
    )
    return Response(status=status.HTTP_201_CREATED, message="Rezume has been updated")


@router.delete("/rezume/{rezume_id}")
async def delete_rezume(
    rezume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not current_user.get("is_team_lead"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You have not permission!"
        )

    rezume_from_db = await db.scalar(select(Rezume).where(Rezume.id == rezume_id))

    if rezume_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rezume not in db!"
        )

    await db.execute(delete(Rezume).where(Rezume.id == rezume_id))
    await db.commit()

    return Response(status=status.HTTP_200_OK, message="Rezume has been deleted")


@router.patch(
    "/rezumes/next_stage/{rezume_id}",
    summary="Двигает резюме в следующую стадию",
    response_model=Response,
)
async def move_to_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume_id: int,
):
    rezume_from_bd = await db.scalar(select(Rezume).where(Rezume.id == rezume_id))

    if rezume_from_bd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not rezume"
        )

    max_stage = await db.scalar(select(func.max(Stage.id)))

    if rezume_from_bd.stage_id == max_stage:
        await db.execute(delete(Rezume).where(Rezume.id == rezume_id))
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rezume passed all Stages and has been deleted",
        )

    next_stage = rezume_from_bd.stage_id + 1
    time_for_stage = await db.scalar(
        select(SLASettings.max_time).where(SLASettings.stage_id == next_stage)
    )

    if time_for_stage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Max time from sla_settings not found!",
        )

    if rezume_from_bd.stage_id == 6:
        in_stage_time = datetime.utcnow() - rezume_from_bd.uploadet_ad
    else:
        in_stage_time = (
            datetime.utcnow() - rezume_from_bd.max_time - timedelta(seconds=432000)
        )
    stat = db.scalar((select(Statistic)).filter(Statistic.id == 1))
    if stat is None:
        await db.add()

    max_time = timedelta(seconds=time_for_stage) + datetime.utcnow()
    await db.execute(
        update(Rezume)
        .where(Rezume.id == rezume_id)
        .values(
            stage_id=next_stage,
            max_time=max_time,
        )
    )
    await db.commit()

    return Response(status=status.HTTP_200_OK, message="Rezume's stage + 1")
