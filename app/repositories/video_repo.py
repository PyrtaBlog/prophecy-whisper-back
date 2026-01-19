# app/repositories/video_repo.py
from sqlalchemy.orm import Session
from app.models.video import Video, VideoStatus

class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_if_not_exists(self, video_data: dict) -> bool:
        if self.db.query(Video).filter(Video.id == video_data["id"]).first():
            return False
        video = Video(**video_data)
        self.db.add(video)
        self.db.commit()
        return True

    def update_transcript(self, video_id: str, transcript: str):
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.transcript = transcript
            video.status = VideoStatus.transcript_done
            self.db.commit()

    def update_status(self, video_id: str, status: str):
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.status = status
            self.db.commit()