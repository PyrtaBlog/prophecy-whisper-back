# app/main.py
# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Prophecy Whisper API", version="1.0.0")
app.include_router(api_router, prefix="/v1")

