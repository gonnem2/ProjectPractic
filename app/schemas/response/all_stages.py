from pydantic import BaseModel


class AllStageResponse(BaseModel):
    status: int
    data: list
