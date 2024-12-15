from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from fastapi.params import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.rezume import Rezume
from src.routers.auth.utils import get_current_user
from src.schemas.response.all_rezumes import AllRezumeResponse
from src.schemas.response.rezume_response import RezumeResponse

router = APIRouter(prefix="/crud_rezume")


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

    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes],
    )


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

    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes],
    )


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
    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes],
    )


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

    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes],
    )


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
    return AllRezumeResponse(
        status=status.HTTP_200_OK,
        data=[RezumeResponse.from_orm(i) for i in rezumes_from_db],
    )
