import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "ticket_worker",
    broker=REDIS_URL,
    include=["app.celery_worker"]
)

# IMPORTANT: fire-and-forget configuration
celery_app.conf.update(
    task_ignore_result=True,   # DO NOT wait for results
    result_backend=None,       # Disable backend completely
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
