from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "vpn_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["src.vpn.tasks.billing_tasks"]
)


celery_app.conf.update(
    task_serializer="json",
    accept_container=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
)


celery_app.conf.beat_schedule = {
    "daily-billing": {
        "task": "src.vpn.tasks.billing_tasks.daily_billing_task",
        "schedule": crontab(hour=0, minute=0)
    }
}