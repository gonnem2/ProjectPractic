from fastapi import FastAPI, Depends

from app.routers.auth.auth import router as auth
from app.routers.permission.permission import router as permission
from app.routers.crud.rezume.rezume import router as rezume
from app.routers.crud.vacancy.vacancy import router as vacancy
from app.routers.crud.stage.stage import router as stage
from app.routers.crud.sla.sla_settings import router as sla_settings
from app.routers.statistic.statistics import router as statistic
from app.routers.get_with_filters.get_with_filters import router as get_with_filters


app = FastAPI()
app.include_router(auth)
app.include_router(permission)
app.include_router(vacancy)
app.include_router(rezume)
app.include_router(stage)
app.include_router(sla_settings)
app.include_router(statistic)
app.include_router(get_with_filters)
