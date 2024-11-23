from fastapi import FastAPI
from src.routers.auth.auth import router as auth


app = FastAPI()
app.include_router(auth)
