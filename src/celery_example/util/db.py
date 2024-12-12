import os
import pickle
import shutil

import redis

import numpy as np


class DBConnector:
    def get_data(self, ref):
        ...

    def get_data_ref(self, ref):
        ...

    def get_data_refs(self):
        ...

    def remove_data_ref(self, ref):
        ...

    def set_data(self, ref, data):
        ...

    def get_model(self, ref):
        ...

    def set_model(self, ref, model):
        ...


class RedisConnector(DBConnector):
    def __init__(self):
        self.client = redis.StrictRedis(host="localhost", port=6379, decode_responses=False)

    def get_data(self, ref):
        obj = self.client.hgetall(ref)
        obj = {
            key.decode("utf-8"): value.decode("utf-8")
            for key, value in obj.items()
        }
        file_path = obj["file_path"]
        data = np.genfromtxt(file_path, delimiter=',')
        return data

    def get_data_ref(self, ref):
        return self.client.hgetall(ref)

    def get_data_refs(self):
        keys = self.client.keys()
        filtered_keys = [key for key in keys if key.decode("utf-8").startswith("data_")]
        all_data = {key: self.client.hgetall(key) for key in filtered_keys}
        return all_data

    def remove_data_ref(self, ref):
        ref_obj = self.get_data_ref(ref)
        file_path = ref_obj[b'file_path'].decode("utf-8")
        shutil.rmtree(file_path)
        return self.client.delete(ref) == 1

    def set_data(self, ref, data):
        self.client.hset(ref, mapping=data)

    def get_model(self, ref):
        return pickle.loads(self.client.get(ref))

    def set_model(self, ref, model):
        self.client.set(ref, pickle.dumps(model))
