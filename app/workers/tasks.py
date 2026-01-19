# app/workers/tasks.py
from datetime import datetime, timedelta, timezone
from app.workers.celery_app import celery_app
from app.services.crawler import fetch_and_save_videos
from app.db.session import SessionLocal
from app.models.video import Video

@celery_app.task(bind=True, max_retries=3)
def process_channel_task(self, channel_id: str):
    db = SessionLocal()
    try:
        # Определяем период: за последнюю неделю или с start_date
        now = datetime.now(timezone.utc)
        one_week_ago = now - timedelta(days=7)

        # Получаем start_date из БД
        from app.models.channel import Channel
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            return

        search_start = max(channel.start_date, one_week_ago)

        # Получаем и сохраняем новые видео
        video_ids = fetch_and_save_videos(db, channel_id, search_start)

        # Запускаем транскрипцию для каждого
        for vid in video_ids:
            transcribe_video_task.delay(vid)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def transcribe_video_task(self, video_id: str):
    db = SessionLocal()
    try:
        from app.services.transcriber import transcribe_video_service
        transcript = transcribe_video_service(db, video_id)

        if transcript:
            # 🔥 ЗАПУСКАЕМ AI EXTRACTOR СРАЗУ ПОСЛЕ ТРАНСКРИПЦИИ
            from app.workers.tasks import extract_predictions_task
            extract_predictions_task.delay(video_id, transcript)

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
    finally:
        db.close()

@celery_app.task
def extract_predictions_task(video_id: str, transcript: str):
    """
    Заглушка для AI Extractor.
    Позже замените на вызов LLM.
    """
    print(f"🧠 AI Extractor: processing {video_id} (len={len(transcript)})")
    # TODO: вызов GPT-4o / Claude / вашей модели
    # Сохранение в таблицу `predictions`