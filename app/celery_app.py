from celery import Celery
from app.config import REDIS_URL
import os

celery = Celery(
    "payments_yookassa",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# маршруты задач
celery.conf.task_routes = {
    "app.tasks.sync_payment": {"queue": "payments"},
    "app.tasks.sync_all_payments": {"queue": "payments"}
}

# рекомендуемые базовые настройки
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
