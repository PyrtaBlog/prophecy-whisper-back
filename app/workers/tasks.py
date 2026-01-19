from app.workers.celery_app import celery_app
from app.services.crawler import run_daily_crawl
from app.services.transcriber import transcribe_video_service
from app.db.session import SessionLocal

@celery_app.task(bind=True, max_retries=3)
def daily_crawl_task(self):
    db = SessionLocal()
    try:
        run_daily_crawl(db)
    finally:
        db.close()

@celery_app.task(bind=True, max_retries=3)
def transcribe_video_task(self, video_id: str):
    db = SessionLocal()
    try:
        transcribe_video_service(db, video_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))
    finally:
        db.close()