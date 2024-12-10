from fastapi import FastAPI
from celery_example.api.data import router as data_router
from celery_example.api.tasks import router as tasks_router

app = FastAPI()
app.include_router(data_router, prefix="/data", tags=["data"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
