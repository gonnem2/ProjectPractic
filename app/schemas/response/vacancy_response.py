from datetime import datetime

from pydantic import BaseModel


class VacancyResponse(BaseModel):
    title: str
    id: int
    user_id: int
    updated_at: datetime | None = None
    description: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
