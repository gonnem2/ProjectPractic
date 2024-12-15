from pydantic import BaseModel
from typing import Optional


class CreateVacancy(BaseModel):
    title: str
    description: str
