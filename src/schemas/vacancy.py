from pydantic import BaseModel
from typing import Optional


class CreateVacancy(BaseModel):
    title: str
    description: str
    updatet_at: Optional[str] = None
