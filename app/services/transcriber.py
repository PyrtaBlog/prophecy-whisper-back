from sqlalchemy.orm import Session
from app.repositories.video_repo import VideoRepository
from app.external.transcript import get_transcript_text
from app.models.video import VideoStatus

def transcribe_video_service(db: Session, video_id: str):
    try:
        transcript = get_transcript_text(video_id)
        repo = VideoRepository(db)
        repo.update_transcript(video_id, transcript)
        return transcript
    except Exception as e:
        print(f"❌ Failed to transcribe {video_id}: {e}")
        repo = VideoRepository(db)
        repo.update_status(video_id, VideoStatus.error)
        raise