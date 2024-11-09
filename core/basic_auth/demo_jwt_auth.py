import secrets
from sys import prefix

from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel

from core.schemas import UserSchemas
from core.basic_auth.utils import hash_password, encode_jwt, validate_password


class Token(BaseModel):
    acsess_toke: str
    token_type: str


tokens: [Token] = list()

router = APIRouter(prefix="/jwt", tags=["JWT"])


jhon = UserSchemas(
    username="jhon",
    password=hash_password("12456"),
    email="gonne@jaik.ru",
)
alex = UserSchemas(
    username="alex",
    password=hash_password("123456"),
    email="alex@jaik.ru",
)
users_db: dict[str, UserSchemas] = {jhon.username: jhon, alex.username: alex}


def validate_auth_user_login(username: str = Form(), password: str = Form()):
    unaut_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не правильно!",
    )
    if not (user := users_db.get(username)):
        raise unaut_exception
    if validate_password(password, users_db.get(username).password):
        return user

    raise unaut_exception


@router.post("/login", response_model=Token)
def login_jwt(user: UserSchemas = Depends(validate_auth_user_login)):
    jwt_payload = {"sub": user.username, "username": user.username, "email": user.email}
    acsecc_token = encode_jwt(
        jwt_payload,
    )
    tokens.append(Token(acsess_toke=acsecc_token, token_type="Bearer"))
    return Token(acsess_toke=acsecc_token, token_type="Bearer")


def create_user(username: str = Form(), password: str = Form(), email: str = Form()):
    unaut_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Ошибка",
    )
    if user := users_db.get(username):
        raise unaut_exception
    else:
        user = UserSchemas(
            username=username,
            password=hash_password(password),
            email=email,
        )
        users_db[username] = user


@router.post("/registration")
def registration(user: UserSchemas = Depends(create_user)):
    return HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Пользователь успешно зарегистрирован",
    )


@router.get("/show-tokens")
def show():
    return tokens
