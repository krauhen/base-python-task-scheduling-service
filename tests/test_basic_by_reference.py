import time

import numpy as np
import requests

from celery_example.models.tasks import TrainModel, PredictModel


def test_basic_by_value():
    print()
    print()
    print("Upload Training data...")

    url = "http://localhost:8000/data/add_data_from_values"

    X = np.random.randint(-200, 200, size=(1000, 2)) / 100
    data = X.tolist()

    response = requests.put(url, params={"description": "Training data X."}, json=data)

    if response.status_code == 200:
        response = response.json()
        X_ref = response["data_ref"]
        print(f"X_ref: {X_ref}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Upload Ground Truth data...")

    url = "http://localhost:8000/data/add_data_from_values"

    y = X[:, 0:1] * X[:, 1:2]
    data = y.tolist()

    response = requests.put(url, params={"description": "Ground Truth data y."}, json=data)

    if response.status_code == 200:
        response = response.json()
        y_ref = response["data_ref"]
        print(f"y_ref: {y_ref}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Upload Test data...")

    url = "http://localhost:8000/data/add_data_from_values"

    data = X[:3].tolist()

    response = requests.put(url, params={"description": "Test data X."}, json=data)

    if response.status_code == 200:
        response = response.json()
        X_test_ref = response["data_ref"]
        print(f"X_test_ref: {X_test_ref}")
    else:
        return False
    print("...done!")
    print()

    ######################################################
    print("Fit Model...")

    url = "http://localhost:8000/tasks/add_task?task_type=FIT"

    data = dict()
    data["X_ref"] = X_ref
    data["y_ref"] = y_ref

    response = requests.put(url, json=data)

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

    data = dict()
    data["X_ref"] = X_test_ref
    data["model_ref"] = model_ref

    response = requests.put(url, json=data)

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
