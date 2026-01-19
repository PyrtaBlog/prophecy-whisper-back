import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "prophecy_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "daily-crawl": {
            "task": "app.workers.tasks.daily_crawl_task",
            "schedule": crontab(hour=2, minute=0),
        },
    },
)

celery_app.autodiscover_tasks(["app.workers"])