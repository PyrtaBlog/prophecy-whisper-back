# app/external/audio.py
import os
import tempfile
from yt_dlp import YoutubeDL


def download_audio(video_id: str) -> str:
    """
    Скачивает аудио из YouTube видео с отключенной SSL-проверкой.
    """
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{video_id}.mp3")

    proxy_url = "http://brd-customer-hl_1b7ce324-zone-residential_proxy1:pdk30eueypwc@brd.superproxy.io:33335"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'proxy': proxy_url,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
        # Отключаем SSL-проверку через yt-dlp
        'no_check_certificate': True,
        'socket_timeout': 60,
        'retries': 3,
        # Дополнительные опции для обхода блокировок
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Audio file not created for {video_id}")

    return output_path