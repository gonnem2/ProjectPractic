from datetime import datetime, timedelta
from pydantic import BaseModel


class SetTime(BaseModel):
    under: datetime = datetime.utcnow() - timedelta(days=600)
    upper: datetime = datetime.utcnow() + timedelta(days=600)
