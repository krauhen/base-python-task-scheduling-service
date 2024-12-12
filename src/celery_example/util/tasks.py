import uuid
import pickle
from enum import Enum
from typing import Union

from celery_example.util.db import RedisConnector
from src.celery_example.celery.celery import celery_handle
from sklearn.linear_model import LinearRegression

storage = RedisConnector()


class TaskTypes(str, Enum):
    FIT = "FIT"
    PREDICT = "PREDICT"


@celery_handle.task
def fit(X=None, y=None, X_ref: Union[None, str] = None, y_ref: Union[None, str] = None):
    try:
        if X_ref is not None:
            X = storage.get_data(X_ref)
        if y_ref is not None:
            y = storage.get_data(y_ref)

        regressor = LinearRegression().fit(X, y)
        score = regressor.score(X, y)

        model_ref = "model_" + str(uuid.uuid4())
        storage.set_model(model_ref, regressor)

        return {"model_ref": model_ref, "score": score}
    except Exception as e:
        return {"error": str(e)}


@celery_handle.task
def predict(model_ref: str, X=None, X_ref: Union[None, str] = None):
    try:
        if X_ref is not None:
            X = storage.get_data(X_ref)

        regressor = storage.get_model(model_ref)

        y = regressor.predict(X)
        y = y.tolist()

        return {"y": y}
    except Exception as e:
        return {"error": str(e)}


task_executors = dict()
task_executors[TaskTypes.FIT] = fit
task_executors[TaskTypes.PREDICT] = predict
