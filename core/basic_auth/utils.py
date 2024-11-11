from datetime import timedelta, datetime
from typing import Optional

import jwt
from core.settings import settings
import bcrypt


def encode_jwt(
    payload: dict,
    key: str = settings.auth_jwt.private_key_path.read_text(),
    algoritm: str = settings.auth_jwt.algoritm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_time_delta: Optional[timedelta] = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_time_delta:
        expire = now + expire_time_delta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        expire=expire.timestamp(),
        iat=now.timestamp(),
    )

    encoded = jwt.encode(to_encode, key, algorithm=algoritm)
    return encoded


def decode_jwt(
    token,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algoritm: str = settings.auth_jwt.algoritm,
):
    decoded = jwt.decode(token, public_key, algoritms=[algoritm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def validate_password(new_password: str, hashd_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=new_password.encode(), hashed_password=hashd_password
    )
