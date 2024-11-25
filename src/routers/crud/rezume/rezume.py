from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing import Annotated

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

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
