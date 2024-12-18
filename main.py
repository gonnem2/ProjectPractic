from fastapi import FastAPI, Depends

from src.routers.auth.auth import router as auth
from src.routers.permission.permission import router as permission
from src.routers.crud.rezume.rezume import router as rezume
from src.routers.crud.vacancy.vacancy import router as vacancy
from src.routers.crud.stage.stage import router as stage
from src.routers.crud.sla.sla_settings import router as sla_settings
from src.routers.statistic.statistics import router as statistic
from src.routers.get_with_filters.get_with_filters import router as get_with_filters


app = FastAPI()
app.include_router(auth)
app.include_router(permission)
app.include_router(vacancy)
app.include_router(rezume)
app.include_router(stage)
app.include_router(sla_settings)
app.include_router(statistic)
app.include_router(get_with_filters)
