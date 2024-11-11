from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, Text
from core.settings import settings
from core.DataBase.models.models import Base, UserBase
from core.basic_auth.auth import router as auth_router
from core.basic_auth.demo_jwt_auth import router as jwt_router
import uvicorn

print(settings.db_url)

engine = create_engine(
    "postgresql+psycopg2://postgres:andrei2006909@localhost:5432/postgres"
)


def create_all(engine):
    return Base.metadata.create_all(engine)


create_all(engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(jwt_router)


@app.get("/user/create")
def say_hello(name, job_title, pasword, key):
    res = {}
    with Session(engine) as session:
        new_user = UserBase(
            name=name, job_title="Programmist", hashed_pass="12sfdsfa@424"
        )
        session.add(new_user)
        res = session.get(UserBase, 1)
        session.commit()
    return res


@app.get("/get")
def return_bd(name):
    res = {}
    with Session(engine) as session:
        res = (
            session.execute(select(UserBase).where(UserBase.name == name))
            .scalars()
            .all()
        )

    return res

if __name__ == "__main__":
    uvicorn.run(app)