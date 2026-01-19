# trigger.py
from app.workers.tasks import daily_crawl_task
daily_crawl_task.delay()
print("✅ Задача отправлена в очередь")