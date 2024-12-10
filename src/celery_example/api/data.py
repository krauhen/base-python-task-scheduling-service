from typing import List, Any

from fastapi import APIRouter, UploadFile, File, Form

from celery_example.lib.data import (add_data_from_file,
                                     add_data_from_values,
                                     get_data_ref,
                                     get_data_refs, remove_data,
                                     update_data)

router = APIRouter()


@router.put("/add_data_from_file")
async def add_data_from_file_endpoint(
        data: UploadFile = File(...),
        description: str = Form(...)
):
    return await add_data_from_file(data, description)


@router.put("/add_data_from_values")
async def add_data_from_values_endpoint(
        data: List[List[Any]],
        description: str
):
    return await add_data_from_values(data, description)


@router.get("/get_data_ref")
async def get_data_ref_endpoint(data_ref: str):
    return await get_data_ref(data_ref)


@router.get("/get_data_refs")
async def get_data_refs_endpoint():
    return await get_data_refs()


@router.delete("/remove_data")
async def remove_data_endpoint(data_ref: str):
    return await remove_data(data_ref)


@router.patch("/update_data")
async def update_data_endpoint(data_ref: str,
                               data: UploadFile = File(...),
                               description: str = Form(...)):
    return await update_data(data_ref, data, description)
