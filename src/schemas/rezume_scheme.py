from pydantic import BaseModel
from typing import Optional


class CreateRezume(BaseModel):
    source: str
    text: str
    vacancy_id: int
