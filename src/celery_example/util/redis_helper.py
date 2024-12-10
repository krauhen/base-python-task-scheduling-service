import numpy as np


def get_data_from_redis(ref, redis_client):
    obj = redis_client.hgetall(ref)
    obj = {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in obj.items()
    }
    file_path = obj["file_path"]
    data = np.genfromtxt(file_path, delimiter=',')
    return data