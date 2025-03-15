import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_project.settings")

celery_app = Celery("crypto_app_ws")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "clean-db-every-10-days": {
        "task": "crypto_app_ws.tasks.clean_old_data",
        "schedule": crontab(day_of_month="*/10", hour=10, minute=0),
    }
}
