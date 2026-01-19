# Используем актуальный Python образ с обновлёнными CA-сертификатами
FROM python:3.11-slim-bookworm

# Устанавливаем системные зависимости для yt-dlp и gevent
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Устанавливаем пользователя без root-прав
RUN addgroup --system app && adduser --system --group app
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Меняем владельца файлов
RUN chown -R app:app /app
USER app

# Экспонируем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]