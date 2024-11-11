from pathlib import Path
from pydantic.v1 import BaseModel

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "-jwt-public.pem"
    algoritm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings:
    db_url: str = "postgresql+psycopg2://andrejkamnskij:asdqwe@localhost/users"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
