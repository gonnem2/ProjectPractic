from datetime import datetime

from pydantic import BaseModel


class CreateSLA(BaseModel):
    max_time: int
    stage_id: int
