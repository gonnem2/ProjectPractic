from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.models.vacancy import Vacancy
from src.models.rezume import Rezume
from src.routers.auth.utils import get_current_user
from src.schemas.request.vacancy import CreateVacancy
from src.schemas.response.response import Response
from src.schemas.response.all_response import ResponseAll
from src.schemas.response.vacancy_response import VacancyResponse

router = APIRouter(prefix="/crud", tags=["Vacancy"])


@router.post(
    "/vacancy",
    status_code=status.HTTP_201_CREATED,
    summary="🚧 Создает вакансию",
    response_model=Response,
)
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
    return Response(status=status.HTTP_201_CREATED, message="Vacancy created")


@router.get(
    "/vacancy",
    summary="Возвращает все вакансии!",
    response_model=ResponseAll,
)
async def get_all_vacancies(db: Annotated[AsyncSession, Depends(get_db)]):
    vacancies = await db.scalars(select(Vacancy))
    return ResponseAll(
        status=status.HTTP_200_OK,
        data=[VacancyResponse.from_orm(i) for i in vacancies.all()],
    )


@router.get(
    "/vacancy/name/{vacancy_title}",
    summary="Возвращает вакансию по названию",
    response_model=VacancyResponse,
)
async def get_vacancy_by_title(
    vacancy_title: Annotated[str, Path()], db: Annotated[AsyncSession, Depends(get_db)]
):
    vacancy = await db.scalar(select(Vacancy).where(Vacancy.title == vacancy_title))
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found!"
        )
    return VacancyResponse(
        title=vacancy.title,
        id=vacancy.id,
        user_id=vacancy.user_id,
        updated_at=vacancy.updated_at,
        description=vacancy.description,
        created_at=vacancy.created_at,
    )


@router.get(
    "/vacancy/{vacancy_id}",
    summary="Возвращает вакансию по id",
    response_model=VacancyResponse,
)
async def get_vacancy_by_id(
    vacancy_id: Annotated[int, Path()], db: Annotated[AsyncSession, Depends(get_db)]
):
    vacancy = await db.scalar(select(Vacancy).where(Vacancy.id == vacancy_id))
    if not vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found!"
        )
    return VacancyResponse(
        title=vacancy.title,
        id=vacancy.id,
        user_id=vacancy.user_id,
        updated_at=vacancy.updated_at,
        description=vacancy.description,
        created_at=vacancy.created_at,
    )


@router.delete("/vacancy/{id}", summary="❌ Удалить вакансию", response_model=Response)
async def delete_vacancy(
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not current_user.get("is_team_lead"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You have not permission!"
        )

    vacancy_from_db = await db.scalar(select(Vacancy).where(Vacancy.id == id))

    if vacancy_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Have not that vacancy in DB"
        )
    await db.execute(delete(Rezume).where(Rezume.vacancy_id == id))
    await db.execute(delete(Vacancy).where(Vacancy.id == id))
    await db.commit()

    return Response(status=status.HTTP_200_OK, message="Vacancy has been deleted")
