from datetime import datetime
from typing import Optional

from pydantic.v1 import BaseModel
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    pass


class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    job_title: Mapped[str] = mapped_column(String(30))
    hashed_pass: Mapped[str] = mapped_column(String(200))


class VacancyBase(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vacancy_title: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(120))
    experience: Mapped[int] = mapped_column()


class RezumeBase(Base):
    __tablename__ = "rezumes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vacancy_id: Mapped[str] = mapped_column(ForeignKey("vacancies.id"))
    description: Mapped[Optional[str]] = mapped_column(String(120))
    experience: Mapped[Optional[str]] = mapped_column()
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StageBase(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    open: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))
    watched: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))
    interview: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))
    technical_interview: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))
    technical_interview_passed: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))
    offer: Mapped[int] = mapped_column(ForeignKey("rezumes.id"))


# - открыта (загружена в систему)
# - изучена (HR просмотрел резюме)
# - интервью (Рекрут приглашен на интервью с HR)
# - прошли интервью (Рекрут прошел интервью с HR)
# - техническое собеседования (Рекрут приглашен на собеседование с заказчиком вакансии)
# - пройдено техническое собеседование (Рекрут прошел техническое резюме)
# - оффер (HR выслал предложение рекруту)
