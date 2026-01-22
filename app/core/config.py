# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    # YouTube API
    YOUTUBE_API_KEY: str

    BRIGHT_DATA_USERNAME: str
    BRIGHT_DATA_PASSWORD: str

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        # Запрещаем неизвестные поля (по умолчанию)
        extra = "forbid"


settings = Settings()