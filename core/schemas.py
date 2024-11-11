import pydantic
from blib2to3.pgen2.token import COMMA
from cffi.model import VoidType
from psycopg.types.multirange import NumericMultirange
from pydantic import EmailStr, ConfigDict


class UserSchemas(pydantic.BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
