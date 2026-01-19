# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.session import engine, Base

app = FastAPI(title="Prophecy Whisper API", version="1.0.0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте (ТОЛЬКО для MVP!)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    yield
    # Закрываем соединения (если нужно)
    await engine.dispose()
app.include_router(api_router, prefix="/v1")

