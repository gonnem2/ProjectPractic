from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy import select
from fastapi import HTTPException, status, Depends
from datetime import timedelta, datetime, timezone
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Annotated
from .security import oauth2_scheme

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITM = os.getenv("ALGHORITM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(
    db: AsyncSession,
    username: str,
    password: str,
    model,
):
    user = await db.scalar(select(model).where(model.username == username))
    if (
        not user
        or not user.is_active
        or not bcrypt_context.verify(password, user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Autheniicate": "Bearer"},
        )
    return user


async def access_token(
    username: str,
    user_id: int,
    is_hr: bool,
    is_team_lead: bool,
    expirse_data: timedelta,
):
    encode = {
        "sub": username,
        "user_id": user_id,
        "is_hr": is_hr,
        "is_team_lead": is_team_lead,
    }

    expires = datetime.now(timezone.utc) + expirse_data
    encode.update({"exp": expires})

    return encode


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGHORITM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        is_hr: str = payload.get("is_hr")
        is_team_lead: str = payload.get("is_team_lead")
        expire = payload.get("exp")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        return {
            "username": username,
            "id": user_id,
            "is_hr": is_hr,
            "is_team_lead": is_team_lead,
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired!"
        )
    # except JWTError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
    #     )
