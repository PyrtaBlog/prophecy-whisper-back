# app/external/transcript.py
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig


def get_transcript_text(video_id: str) -> str:
    """
    Получает автогенерированные субтитры через youtube-transcript-api + Bright Data.
    Использует официальную поддержку прокси.
    """
    username = os.getenv("BRIGHT_DATA_USERNAME")
    password = os.getenv("BRIGHT_DATA_PASSWORD")

    if not username or not password:
        raise ValueError("Bright Data credentials missing in .env")

    # Формируем URL прокси (порт 33335 из твоего скриншота)
    proxy_url = f"http://{username}:{password}@brd.superproxy.io:33335"

    # Настраиваем прокси через официальный конфиг
    proxy_config = GenericProxyConfig(
        http_url=proxy_url,
        https_url=proxy_url
    )

    try:
        # Создаём API-клиент с прокси
        ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

        # Получаем список субтитров
        transcript_list = ytt_api.list(video_id)

        # Ищем автогенерированные субтитры (русский → английский)
        auto_transcript = transcript_list.find_generated_transcript(['ru', 'en'])

        # Загружаем данные
        fetched = auto_transcript.fetch()

        # Собираем текст (каждый элемент - dict с ключом 'text')
        text = " ".join([s['text'] for s in fetched])
        return text

    except Exception as e:
        raise ValueError(f"Failed to fetch transcript for {video_id}: {e}")