import time

import numpy as np
import requests

from celery_example.models.tasks import TrainModel, PredictModel


def test_basic_by_value():
    print()
    print()
    print("Fit Model...")

    url = "http://localhost:8000/tasks/add_task?task_type=FIT"

    X = np.random.randint(-200, 200, size=(1000, 2)) / 100
    y = X[:, 0:1] * X[:, 1:2]

    data = TrainModel(X=X.tolist(), y=y.tolist())

    response = requests.put(url, json=data.model_dump())

    if response.status_code == 200:
        response = response.json()
        task_id = response["task_id"]
        print(f"task_id: {task_id}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Get TRAIN Task information...")

    url = f"http://localhost:8000/tasks/get_task"

    response = requests.get(url, params={"task_id": task_id})

    if response.status_code == 200:
        response = response.json()
        status = response["status"]
        print(status)
        while status in ["Pending"]:
            print(status)
            response = requests.get(url, params={"task_id": task_id})
            response = response.json()
            status = response["status"]
            time.sleep(1)

        model_ref = response["result"]["model_ref"]
        print(f"model_ref: {model_ref}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Predict with Model...")

    url = "http://localhost:8000/tasks/add_task?task_type=PREDICT"

    X = np.random.randint(-200, 200, size=(10, 2)) / 100

    data = PredictModel(model_ref=model_ref, X=X.tolist())

    response = requests.put(url, json=data.model_dump())

    if response.status_code == 200:
        response = response.json()
        task_id = response["task_id"]
        print(f"task_id: {task_id}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Get PREDICT Task information...")

    url = f"http://localhost:8000/tasks/get_task"

    response = requests.get(url, params={"task_id": task_id})

    if response.status_code == 200:
        response = response.json()
        status = response["status"]
        print(status)
        while status in ["Pending"]:
            print(status)
            response = requests.get(url, params={"task_id": task_id})
            response = response.json()
            status = response["status"]
            time.sleep(1)

        y = response["result"]["y"]
        print(f"y: {y}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
