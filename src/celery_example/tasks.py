import uuid
from enum import Enum
from typing import Union

from src.celery_example.celery import celery_handle
from src.celery_example.db import fake_db
from sklearn.linear_model import LinearRegression


class TaskTypes(str, Enum):
    FIT = "FIT"
    PREDICT = "PREDICT"


@celery_handle.task
def fit(X=None, y=None, X_ref: Union[None, str] = None, y_ref: Union[None, str] = None):
    if X_ref is not None:
        # X = fake_db[X_ref]
        raise NotImplementedError("This is not implemented yet.")

    if y_ref is not None:
        # y = fake_db[y_ref]
        raise NotImplementedError("This is not implemented yet.")

    regressor = LinearRegression().fit(X, y)
    score = regressor.score(X, y)

    model_ref = str(uuid.uuid4())
    fake_db[model_ref] = regressor

    return {"model_ref": model_ref, "score": score}


@celery_handle.task
def predict(model_ref: str, X=None, X_ref: Union[None, str] = None):
    if X_ref is not None:
        # X = fake_db[X_ref]
        raise NotImplementedError("This is not implemented yet.")

    regressor = fake_db[model_ref]
    y = regressor.predict(X)
    y = y.tolist()

    return {"y": y}


task_executors = dict()
task_executors[TaskTypes.FIT] = fit
task_executors[TaskTypes.PREDICT] = predict
