from enum import Enum

from src.celery import celery_handle


class TaskTypes(str, Enum):
    TRAIN = "TRAIN"


@celery_handle.task
def train(text: str):
    return {"text": text}


task_executors = dict()
task_executors[TaskTypes.TRAIN] = train
