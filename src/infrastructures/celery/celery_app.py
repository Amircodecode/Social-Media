# src/infrastructures/celery/celery_app.py
import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "social_media",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.infrastructures.celery.tasks"],
)

celery_app.conf.beat_schedule = {
    "delete-unverified-users-daily": {
        "task": "src.infrastructures.celery.tasks.delete_unverified_users_task",
        "schedule": crontab(hour=0, minute=0),
    },
    "delete-old-articles-monthly": {
        "task": "src.infrastructures.celery.tasks.delete_old_articles_task",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
}
celery_app.conf.timezone = "UTC"
