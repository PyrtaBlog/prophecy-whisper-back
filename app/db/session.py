import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# УБЕРИТЕ значение по умолчанию или сделайте его для Docker
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Для локальной разработки БЕЗ Docker
    DATABASE_URL = "postgresql://prophecy:whisper_secret@localhost:5432/prophecy_db"
else:
    # Убедимся, что в Docker используется правильный хост
    pass

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()