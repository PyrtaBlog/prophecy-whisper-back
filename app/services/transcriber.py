# app/services/transcriber.py
import logging
import os
from sqlalchemy.orm import Session
from app.repositories.video_repo import VideoRepository
from app.models.video import VideoStatus
from app.external.audio import download_audio
from app.external.transcriber import get_transcript_from_audio

logger = logging.getLogger(__name__)


def transcribe_video_service(db: Session, video_id: str):
    try:
        logger.info(f"🎧 Starting audio download for {video_id}")
        audio_path = download_audio(video_id)
        logger.info(f"✅ Audio downloaded: {audio_path}")

        logger.info(f"🗣️ Starting transcription for {video_id}")
        transcript = get_transcript_from_audio(audio_path)
        logger.info(f"✅ Transcription completed (length: {len(transcript)})")

        repo = VideoRepository(db)
        repo.update_transcript(video_id, transcript)

        # Удаляем временный файл
        os.remove(audio_path)
        logger.info(f"🧹 Cleaned up audio file for {video_id}")

    except Exception as e:
        error_msg = f"❌ Transcription failed for {video_id}: {e}"
        logger.error(error_msg)
        repo = VideoRepository(db)
        repo.update_status(video_id, VideoStatus.error)
        raise