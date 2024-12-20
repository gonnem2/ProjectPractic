from pydantic import BaseModel


class AllRezumeResponse(BaseModel):
    status: int
    data: list

    class Config:
        orm_mode = True
        from_attributes = True
