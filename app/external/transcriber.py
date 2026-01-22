# app/external/transcriber.py
from faster_whisper import WhisperModel

# Загружаем модель один раз (можно вынести в глобальную переменную)
_model = None


def get_transcript_from_audio(audio_path: str) -> str:
    """
    Транскрибирует аудиофайл через Faster Whisper.
    """
    global _model
    if _model is None:
        # Используем small модель для баланса скорость/качество
        # Доступные модели: tiny, base, small, medium, large-v3
        _model = WhisperModel("small", device="cpu", compute_type="int8")

    segments, _ = _model.transcribe(
        audio_path,
        language="ru",  # или "auto" для автоопределения
        beam_size=5,
        vad_filter=True  # улучшает качество за счёт фильтрации тишины
    )

    text = " ".join([segment.text for segment in segments])
    return text.strip()