from fastapi import APIRouter
from app.api.v1 import channels, transcribe, videos, predictions

api_router = APIRouter()
api_router.include_router(channels.router, prefix="/channels", tags=["channels"])
api_router.include_router(transcribe.router, prefix="/transcribe", tags=["transcribe"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])