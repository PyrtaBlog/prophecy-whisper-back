# app/api/v1/channels.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timezone
from app.db.session import SessionLocal
from app.models.channel import Channel
from app.external.youtube import extract_channel_id_from_url, get_channel_name
from app.workers.tasks import process_channel_task  # ← НОВАЯ ЗАДАЧА

router = APIRouter()

class ChannelAddRequest(BaseModel):
    url: str
    start_date: str
    description: str = ""

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_channel(request: ChannelAddRequest):
    try:
        channel_id = extract_channel_id_from_url(request.url)
        start_date = datetime.fromisoformat(request.start_date).replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")

    db = SessionLocal()
    try:
        existing = db.query(Channel).filter(Channel.id == channel_id).first()
        if existing:
            raise HTTPException(status_code=409, detail="Channel already exists")

        name = get_channel_name(channel_id)
        new_channel = Channel(
            id=channel_id,
            name=name,
            description=request.description,
            start_date=start_date
        )
        db.add(new_channel)
        db.commit()

        # 🔥 ЗАПУСКАЕМ ОБРАБОТКУ СРАЗУ
        process_channel_task.delay(channel_id)

        return {
            "message": "Channel added and processing started",
            "channel_id": new_channel.id,
            "name": new_channel.name,
            "start_date": new_channel.start_date.isoformat(),
            "description": new_channel.description
        }
    finally:
        db.close()