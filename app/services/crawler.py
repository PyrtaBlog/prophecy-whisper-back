# app/services/crawler.py
from datetime import datetime, timezone
from app.repositories.video_repo import VideoRepository
from app.external.youtube import get_latest_videos

def fetch_and_save_videos(db, channel_id: str, start_date: datetime):
    """
    Находит новые видео с канала с даты start_date и сохраняет их.
    Возвращает список ID новых видео.
    """
    repo = VideoRepository(db)

    # Преобразуем в часы для YouTube API
    now = datetime.now(timezone.utc)
    hours_back = int((now - start_date).total_seconds() / 3600)
    hours_back = min(hours_back, 720)  # максимум 30 дней

    videos = get_latest_videos(channel_id, hours=hours_back)

    new_video_ids = []
    for v in videos:
        # Проверяем, не обработано ли уже
        if not repo.video_exists(v["id"]):
            created = repo.create_if_not_exists({
                "id": v["id"],
                "channel_id": channel_id,
                "title": v["title"],
                "publish_date": v["publish_date"]
            })
            if created:
                new_video_ids.append(v["id"])

    return new_video_ids