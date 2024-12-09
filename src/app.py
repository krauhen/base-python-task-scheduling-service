from fastapi import FastAPI
from src.task_handler import *

app = FastAPI()


@app.get("/tasks/get_task_ids")
async def get_task_ids_endpoint() -> List[str]:
    return await get_task_ids()


@app.put("/tasks/add_task")
async def add_task_endpoint(text: str, task_type: TaskTypes) -> Dict[str, str]:
    if task_type in TaskTypes:
        return await add_task({"text": text}, task_type)
    else:
        raise Exception("No valid task type.")


@app.get("/tasks/get_task")
async def get_task_endpoint(task_id: str) -> Dict[str, Union[str, int, Dict[str, Union[int, float]]]]:
    return await get_task(task_id)


@app.delete("/tasks/remove_task")
async def remove_task_endpoint(task_id: str) -> bool:
    result = await remove_task(task_id)
    if not result:
        raise Exception(f"Task with task_id: {task_id} not found.")
    else:
        return result
