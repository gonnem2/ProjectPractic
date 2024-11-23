from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import insert, select
from jose import jwt, ExpiredSignatureError
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.core.db import get_db
from src.schemas.user_scheme import CreateUser
from src.models.user import User
from src.schemas.token_schemas import Token
from .utils import get_user, access_token, get_current_user

# from .security import oauth2_scheme

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGHORITM = os.getenv("ALGHORITM")

router = APIRouter(prefix="/auth", tags=["Authorization"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser
):
    await db.execute(
        insert(User).values(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            username=create_user.username,
            email=create_user.email,
            hashed_password=bcrypt_context.hash(create_user.password),
        )
    )
    await db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.get("/get_users")
async def get_all_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if current_user.get("is_hr"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    users = await db.scalars(select(User))
    return users.all()


@router.post("/token")
async def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await get_user(db, form_data.username, form_data.password, User)
    token = await access_token(
        user.username,
        user.id,
        user.is_hr,
        user.is_team_lead,
        timedelta(minutes=20),
    )
    return {
        "access_token": jwt.encode(token, SECRET_KEY, algorithm=ALGHORITM),
        "token_type": "bearer",
    }


@router.get("/asd")
async def asd(user: Annotated[dict, Depends(get_current_user)]):
    return user
