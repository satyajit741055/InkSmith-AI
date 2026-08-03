from celery import Celery 
from app.config import settings

celery_app = Celery(
    "blog_task",
    broker = settings.REDIS_URL,
    backend = settings.REDIS_URL,
    include=["app.tasks.blog_tasks"],  # so Celery discovers your task module automatically
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,      # lets you see "STARTED" state, useful for progress updates
    result_expires=3600,          # avoid Redis filling up with old results forever
)