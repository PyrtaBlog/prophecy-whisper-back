import time
import random
from typing import cast
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.workers.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.channel import Channel
from app.services.crawler import fetch_and_save_videos


@celery_app.task(bind=True, max_retries=3)
def process_channel_task(self, channel_id: str):
    db: Session = SessionLocal()
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")

        start_date_utc = cast(datetime, channel.start_date)
        now = datetime.now(timezone.utc)
        one_month_ago = now - timedelta(days=30)
        search_start = max(start_date_utc, one_month_ago)

        new_video_ids = fetch_and_save_videos(db, channel_id, search_start)

        for video_id in new_video_ids:
            # Добавляем небольшую задержку между задачами
            time.sleep(1)
            transcribe_video_task.delay(video_id)

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()


@celery_app.task(bind=True, max_retries=3)
def transcribe_video_task(self, video_id: str):
    """
    Транскрибирует видео с защитой от 429 ошибок:
    - Случайная задержка
    - Использует Webshare + cookies (настраивается в transcript.py)
    """
    # Rate limiting: случайная пауза 1-3 секунды
    time.sleep(random.uniform(1.0, 3.0))

    db = SessionLocal()
    try:
        from app.services.transcriber import transcribe_video_service
        transcribe_video_service(db, video_id)
    except Exception as exc:
        db.rollback()
        # Увеличиваем время повтора при 429
        if "429" in str(exc) or "Too Many Requests" in str(exc):
            raise self.retry(exc=exc, countdown=300)  # 5 минут
        else:
            raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()