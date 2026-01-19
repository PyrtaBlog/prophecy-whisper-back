from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.video import Video
from app.models.channel import Channel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    result = []
    for v in videos:
        channel = db.query(Channel).filter(Channel.id == v.channel_id).first()
        result.append({
            "video_id": v.id,
            "video_title": v.title,
            "publish_date": v.publish_date.isoformat() if v.publish_date else None,
            "channel_name": channel.name if channel else "Unknown",
            "status": v.status,
            "has_transcript": v.transcript is not None
        })
    return {"videos": result}