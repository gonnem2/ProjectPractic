from typing import Optional

import pydantic
from pydantic import EmailStr, ConfigDict


class UserSchemas(pydantic.BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: Optional[EmailStr] = None
    active: bool = True
