import subprocess
import json
import os
import tempfile


def get_transcript_text(video_id: str) -> str:
    """
    Использует yt-dlp для получения автогенерированных субтитров.
    """
    cookies_path = "/app/cookies.txt"
    if not os.path.exists(cookies_path):
        raise ValueError("cookies.txt not found")

    # Увеличиваем таймаут до 120 секунд
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, suffix='.json') as tmp_file:
        cmd = [
            'yt-dlp',
            '--cookies', cookies_path,
            '--write-auto-subs',
            '--skip-download',
            '--sub-format', 'json3',
            '--sub-langs', 'ru,en',
            '--no-warnings',
            '--quiet',  # ← меньше вывода
            '--output', tmp_file.name.replace('.json', ''),
            f'https://www.youtube.com/watch?v={video_id}'
        ]

        try:
            # Увеличиваем таймаут до 120 секунд
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                raise ValueError(f"YT-DLP failed: {result.stderr}")

            # Ищем файл субтитров
            subtitle_file = None
            for ext in ['ru.json3', 'en.json3']:
                candidate = tmp_file.name.replace('.json', f'.{ext}')
                if os.path.exists(candidate):
                    subtitle_file = candidate
                    break

            if not subtitle_file:
                raise ValueError("No automatic captions found")

            with open(subtitle_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Обработка JSON3 формата
                text_parts = []
                for event in data.get('events', []):
                    if 'segs' in event:
                        for seg in event['segs']:
                            if 'utf8' in seg:
                                text_parts.append(seg['utf8'])
                return " ".join(text_parts)

        except subprocess.TimeoutExpired:
            raise ValueError("YT-DLP timeout (120s)")
        except Exception as e:
            raise ValueError(f"YT-DLP failed for {video_id}: {str(e)}")