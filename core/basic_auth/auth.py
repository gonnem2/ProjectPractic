import uuid
from uuid import uuid4
import jwt
from dns.edns import COOKIE
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from typing import Annotated, Any
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from time import time
from more_itertools.recipes import unique

router = APIRouter(prefix="/auth", tags=["AUTH"])

security = HTTPBasic()


my_bd = {"BOB": "qwerty", "admin": "admin777"}
static_tocen = {
    "isgv8fhiksjhgsibsgoash98828184": "BOB",
    "gdssdisgggv8fhiksjhgsibsgoash98828184": "admin",
}


@router.get("/basic_auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    if credentials.username == "gonne" and credentials.password == "qwerty":
        return f"Приветики! {credentials.username}"
    else:
        return "ХУЛИГАН!!"


def get_auth_usernme(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="НЕВЕРНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЛИ ПАРОЛЬ",
        headers={"WWW-Autheticate": "BASIC"},
    )
    if my_bd.get(credentials.username) is None:
        raise unauth_exception
    if secrets.compare_digest(
        my_bd.get(credentials.username).encode(), credentials.password.encode()
    ):
        return credentials.username
    else:
        raise unauth_exception


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="НЕВЕРНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЛИ ПАРОЛЬ",
        headers={"WWW-Autheticate": "BASIC"},
    )
    if static_token not in static_tocen:
        raise unauth_exception
    else:
        return static_tocen.get(static_token)


@router.get("/basic-auth/get_name")
def auth_username(auth_username: str = Depends(get_auth_usernme)):
    return {
        "username": auth_username,
    }


@router.get("/some-http-header-auth")
def http_header_auth(username: str = Depends(get_username_by_static_auth_token)):
    return {
        "message": f"Hi! {username}",
        "username": username,
    }


# login by coockie!!

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "SESSION_ID"


def get_session_id(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="НЕВЕРНОЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ИЛИ ПАРОЛЬ",
        headers={"WWW-Autheticate": "BASIC"},
    )
    if session_id not in COOKIES:
        raise unauth_exception
    return COOKIES[session_id]


def generate_sessionId() -> str:
    return uuid.uuid4().hex


@router.post("/login-coockie")
def basic_auth_by_coockie(
    response: Response,
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_sessionId()
    response.set_cookie(
        COOKIE_SESSION_ID_KEY,
        session_id,
    )
    COOKIES[session_id] = {"username": username, "login_at": time()}
    return {"result": "ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(session: dict = Depends(get_session_id)):
    return {"message": f"Hi {session.get("username")}!"}


@router.get("/coockie-logout")
def cookie_logout(
    response: Response, session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
):
    COOKIES.pop(session_id, None)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return "Ok"
