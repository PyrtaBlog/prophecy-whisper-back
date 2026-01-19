from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from app.db.session import SessionLocal
from app.models.channel import Channel
from app.external.youtube import extract_channel_id_from_url, get_channel_name

router = APIRouter()

class ChannelAddRequest(BaseModel):
    url: str
    start_date: str
    description: str = ""

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_channel(request: ChannelAddRequest):
    try:
        channel_id = extract_channel_id_from_url(request.url)
        start_date = datetime.fromisoformat(request.start_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {e}"
        )

    db = SessionLocal()
    try:
        existing = db.query(Channel).filter(Channel.id == channel_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Channel already exists"
            )

        name = get_channel_name(channel_id)
        new_channel = Channel(
            id=channel_id,
            name=name,
            description=request.description,
            start_date=start_date
        )
        db.add(new_channel)
        db.commit()
        db.refresh(new_channel)
        return {
            "message": "Channel added successfully",
            "channel_id": new_channel.id,
            "name": new_channel.name,
            "start_date": new_channel.start_date.isoformat(),
            "description": new_channel.description
        }
    finally:
        db.close()