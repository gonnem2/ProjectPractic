from datetime import timedelta, datetime

from ecdsa import NIST224p
from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated

from fastapi.params import Query
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.user import User
from src.models.vacancy import Vacancy
from src.models.stage import Stage
from src.models.violation import Violation
from src.models.sla_settings import SLASettings
from src.models.rezume import Rezume
from src.routers.auth.utils import get_current_user
from src.schemas.time_for_filter_scheme import SetTime
from src.schemas.vacancy import CreateVacancy
from src.schemas.rezume_scheme import CreateRezume


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

    return HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="rezume has been uploaded!",
    )


@router.get("/rezume")
async def get_all_rezumes(db: Annotated[AsyncSession, Depends(get_db)]):
    rezumes = await db.scalars(select(Rezume))
    return rezumes.all()


@router.put("/rezume/{rezume_id}")
async def update_rezume(
    rezume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume: CreateRezume,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    await db.execute(
        update(Rezume).values(
            vacancy_id=rezume.vacancy_id,
            source=rezume.source,
            text=rezume.text,
            user_id=current_user.get("id"),
        )
    )
    return {"status_code": status.HTTP_201_CREATED, "detail": "rezume has been updated"}


@router.delete("/rezume/{rezume_id}")
async def delete_rezume(
    rezume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume: CreateRezume,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    rezume_from_db = await db.scalar(select(Rezume).where(Rezume.id == rezume_id))

    if rezume_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rezume not in db!"
        )

    await db.execute(delete(Rezume).where(Rezume.id == rezume_id))
    await db.commit()

    return {
        "Success": True,
    }


@router.get(
    "/rezume/filter/filter_by_stage",
    summary="Возвращает резюме только по определенной стадии",
    tags=["Main Filter Logic"],
)
async def get_rezume_by_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    stage_id: Annotated[int, Query()],
):
    rezumes_from_db = await db.scalars(
        select(Rezume).where(Rezume.stage_id == stage_id)
    )

    rezumes_from_db = rezumes_from_db.all()

    if len(rezumes_from_db) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not that's rezume's"
        )
    return {"Success": "True", "data": rezumes_from_db}


@router.patch(
    "/rezumes/next_stage/{rezume_id}",
    summary="Двигает резюме в следующую стадию",
)
async def move_to_stage(
    db: Annotated[AsyncSession, Depends(get_db)],
    rezume_id: int,
):
    rezume_from_bd = await db.scalar(
        select(Rezume.stage_id).where(Rezume.id == rezume_id)
    )

    if rezume_from_bd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not rezume"
        )

    max_stage = await db.scalar(select(func.max(Stage.id)))

    if rezume_from_bd == max_stage:
        await db.execute(delete(Rezume).where(Rezume.id == rezume_id))
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rezume passed all Stages and has been deleted",
        )

    next_stage = rezume_from_bd + 1
    time_for_stage = await db.scalar(
        select(SLASettings.max_time).where(SLASettings.stage_id == next_stage)
    )

    if time_for_stage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Max time from sla_settings not found!",
        )

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

    return {"Success": True, "message": "Rezume's stage + 1"}


@router.get(
    "/rezume/filter/filter_rezume_by_vacancy",
    summary="Возращает резюме по определенной вакансии",
    tags=["Main Filter Logic"],
)
async def get_by_vacancy(
    db: Annotated[AsyncSession, Depends(get_db)],
    vacancy_id: Annotated[int, Query],
    current_user: Annotated[dict, Depends(get_current_user)],
):

    rezumes = (
        await db.scalars(select(Rezume).where(Rezume.vacancy_id == vacancy_id))
    ).all()

    if len(rezumes) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not that rezume's"
        )

    return {"Success": True, "Data": rezumes}


@router.get(
    "/rezume/filter/filter_by_data",
    summary="Возращает резюме опубликованние в промежутке времени",
    tags=["Main Filter Logic"],
)
async def get_by_date(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    under: datetime = None,
    upper: datetime = None,
):
    if under is None:
        under = datetime.utcnow() - timedelta(days=600)
    if upper is None:
        upper = datetime.utcnow() + timedelta(days=600)

    rezumes = (
        await db.scalars(
            select(Rezume).where(
                Rezume.uploadet_ad >= under, Rezume.uploadet_ad <= upper
            )
        )
    ).all()

    if len(rezumes) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not that rezume's"
        )

    return {"Success": True, "Data": rezumes}


@router.get(
    "rezume/sorted/by_date",
    summary="Возвращает все резюме отсортированные по дате создания",
    tags=["Main Filter Logic"],
)
async def get_sorted_by_date(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    rezumes = (
        await db.scalars(select(Rezume).order_by(Rezume.uploadet_ad.desc()))
    ).all()
    return rezumes


@router.get(
    "/rezume/sorted/by_sla",
    summary="Возвращает все резюме, отсортированные по sla",
    tags=["Main Filter Logic"],
)
async def get_sorted_by_sla(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    rezumes = (await db.scalars(select(Rezume).order_by(Rezume.max_time.desc()))).all()

    if len(rezumes) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not rezumes"
        )

    return {
        "Success": True,
        "data": rezumes,
    }
