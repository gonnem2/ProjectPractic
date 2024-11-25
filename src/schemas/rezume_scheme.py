from pydantic import BaseModel


class CreateRezume(BaseModel):
    source: str
    text: str
    vacancy_id: int
