from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.suite.test_reflection import users

from src.core.db import get_db
from src.models.user import User
from src.models.vacancy import Vacancy
from src.models.stage import Stage
from src.models.violation import Violation
from src.models.sla_settings import SLASettings
from src.models.rezume import Rezume
from src.routers.auth.utils import get_current_user
from src.schemas.vacancy import CreateVacancy
from src.schemas.rezume_scheme import CreateRezume


router = APIRouter(prefix="/crud", tags=["Vacancy"])


@router.post("/vacancy", status_code=status.HTTP_201_CREATED)
async def create_vacancy(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    vacancy: CreateVacancy,
):
    vacancy_from_db = await db.scalar(
        select(Vacancy).where(Vacancy.title == vacancy.title)
    )

    if vacancy_from_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Vacancy already in DB"
        )

    if current_user.get("is_hr"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission"
        )

    vacancy_for_db = Vacancy(
        title=vacancy.title,
        description=vacancy.description,
        user_id=current_user.get("id"),
    )
    db.add(vacancy_for_db)
    await db.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Ok")


@router.get("/vacancy")
async def get_all_vacancies(db: Annotated[AsyncSession, Depends(get_db)]):
    vacancies = await db.scalars(select(Vacancy))
    return vacancies.all()


@router.get("/vacancy/name/{vacancy_title}")
async def get_vacancy_by_title(
    vacancy_title: Annotated[str, Path()], db: Annotated[AsyncSession, Depends(get_db)]
):
    vacancy = await db.scalar(select(Vacancy).where(Vacancy.title == vacancy_title))
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found!"
        )
    return vacancy


@router.get("/vacancy/{vacancy_id}")
async def get_vacancy_by_id(
    vacancy_id: Annotated[int, Path()], db: Annotated[AsyncSession, Depends(get_db)]
):
    vacancy = await db.scalar(select(Vacancy).where(Vacancy.id == vacancy_id))
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found!"
        )
    return vacancy
