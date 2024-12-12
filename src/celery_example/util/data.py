import tempfile
import shutil
import os
import uuid
import csv

from typing import List, Any
from fastapi import UploadFile, File, Form

from celery_example.util.db import RedisConnector

storage = RedisConnector()


async def add_data_from_file(
        data: UploadFile = File(...),
        description: str = Form(...),
        data_ref: str = None
):
    if data_ref is None:
        data_ref = "data_" + str(uuid.uuid4())

    temp_dir = tempfile.gettempdir()
    filename = data.filename
    parts = filename.split(".")
    filename = ".".join(parts[0:-1]) + "_" + data_ref + "." + parts[-1]
    temp_file_path = os.path.join(temp_dir, filename)

    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension != ".csv":
        return {"error": "Only .csv files are allowed"}

    try:
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(data.file, temp_file)

        data = {"description": description, "file_path": temp_file_path, "data_ref": data_ref}
        storage.set_data(data_ref, data)

        return {
            "message": "File uploaded successfully",
            "file_path": temp_file_path,
            "description": description,
            "data_ref": data_ref,
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        data.file.close()


async def add_data_from_values(
        data: List[List[Any]],
        description: str,
):
    data_ref = "data_" + str(uuid.uuid4())

    temp_dir = tempfile.gettempdir()
    filename = data_ref + ".csv"
    temp_file_path = os.path.join(temp_dir, filename)

    try:
        with open(temp_file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        data = {"description": description, "file_path": temp_file_path, "data_ref": data_ref}
        storage.set_data(data_ref, data)

        return {
            "message": "File uploaded successfully",
            "file_path": temp_file_path,
            "description": description,
            "data_ref": data_ref,
        }
    except Exception as e:
        return {"error": str(e)}


async def get_data_ref(data_ref: str):
    try:
        data_obj = storage.get_data_ref(data_ref)
        if not data_obj:
            raise ValueError("Data reference not found.")
        return data_obj
    except Exception as e:
        return {"error": str(e)}


async def get_data_refs():
    try:
        return storage.get_data_refs()
    except Exception as e:
        return {"error": str(e)}


async def remove_data(data_ref: str):
    try:
        return storage.remove_data_ref(data_ref)
    except Exception as e:
        return False


async def update_data(data_ref: str,
                      data: UploadFile = File(...),
                      description: str = Form(...)):
    try:
        return await add_data_from_file(data, description, data_ref)
    except Exception as e:
        return {"error": str(e)}
