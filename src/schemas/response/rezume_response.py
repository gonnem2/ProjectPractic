from datetime import datetime

from pydantic import BaseModel


class RezumeResponse(BaseModel):
    id: int
    text: str
    user_id: int
    max_time: datetime | None
    vacancy_id: int
    source: str
    stage_id: int
    uploadet_ad: datetime | None

    class Config:
        orm_mode = True
        from_attributes = True
