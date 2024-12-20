from pydantic import BaseModel


class ResponseAll(BaseModel):
    status: int
    data: list

    class Config:
        orm_mode = True
        from_attributes = True
