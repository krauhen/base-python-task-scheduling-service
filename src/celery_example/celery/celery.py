from celery import Celery

celery_handle = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["src.celery_example.lib.tasks"]
)
