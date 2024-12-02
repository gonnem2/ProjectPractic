from fastapi import FastAPI
import uvicorn

from src.routers.auth.auth import router as auth
from src.routers.permission.permission import router as permission
from src.routers.crud.rezume.rezume import router as rezume
from src.routers.crud.vacancy.vacancy import router as vacancy
from src.routers.crud.stage.stage import router as stage


app = FastAPI()
app.include_router(auth)
app.include_router(permission)
app.include_router(vacancy)
app.include_router(rezume)
app.include_router(stage)
