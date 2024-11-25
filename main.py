from fastapi import FastAPI
from src.routers.auth.auth import router as auth
from src.routers.permission.permission import router as permission
from src.routers.crud.rezume.rezume import router as rezume
from src.routers.crud.vacancy.vacancy import router as vacancy


app = FastAPI()
app.include_router(auth)
app.include_router(permission)
app.include_router(vacancy)
app.include_router(rezume)
