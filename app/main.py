# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.session import engine, Base

# 🔥 Создаём таблицы при старте приложения (ТОЛЬКО ДЛЯ MVP!)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prophecy Whisper API", version="1.0.0")
app.include_router(api_router, prefix="/v1")

