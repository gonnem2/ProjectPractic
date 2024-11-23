from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("DB_URL")

engine = create_async_engine(URL, echo=True)
Session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db() -> AsyncSession:
    async with Session() as session:
        yield session


class Base(DeclarativeBase):
    pass
