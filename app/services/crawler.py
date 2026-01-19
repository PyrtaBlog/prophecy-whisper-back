# app/services/crawler.py
from datetime import datetime, timedelta
from app.repositories.channel_repo import ChannelRepository
from app.repositories.video_repo import VideoRepository
from app.external.youtube import get_latest_videos


def run_daily_crawl(db):
    channel_repo = ChannelRepository(db)
    video_repo = VideoRepository(db)
    channels = channel_repo.get_all()
    now = datetime.utcnow()

    for channel in channels:
        if channel.last_checked_at:
            hours_back = int((now - channel.last_checked_at).total_seconds() / 3600)
        else:
            hours_back = int((now - channel.start_date).total_seconds() / 3600)

        hours_back = min(hours_back, 720)

        try:
            videos = get_latest_videos(channel.id, hours=hours_back)
            for v in videos:
                created = video_repo.create_if_not_exists({
                    "id": v["id"],
                    "channel_id": channel.id,
                    "title": v["title"],
                    "publish_date": v["publish_date"],
                    "status": "transcript_pending"
                })
                if created:
                    # ✅ Отправляем задачу по имени — без импорта!
                    from app.workers.celery_app import celery_app
                    celery_app.send_task("app.workers.tasks.transcribe_video_task", args=[v["id"]])
        except Exception as e:
            print(f"Error crawling channel {channel.id}: {e}")

        channel_repo.update_last_checked(channel.id)