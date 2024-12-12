from typing import Dict, List, Any

from celery.result import AsyncResult
from src.celery_example.util.tasks import task_executors, TaskTypes

all_tasks = dict()


async def get_task_ids() -> List[str]:
    return list(all_tasks.keys())


async def add_task(params: Dict[str, Any], task_type: TaskTypes) -> Dict[str, str]:
    task = task_executors[task_type].delay(**params)

    task_id = task.id
    task_result = AsyncResult(task_id)
    task_state = task_result.status
    all_tasks[task_id] = {"state": task_state}

    return {"task_id": task_id, "task_state": task_state}


async def get_task(task_id: str) -> Dict[str, Any]:
    task_result = AsyncResult(task_id)
    task_state = task_result.status
    all_tasks[task_id] = {"state": task_state}

    if task_state == "PENDING":
        return {"task_id": task_id, "status": "Pending"}
    elif task_state == "SUCCESS":
        return {
            "task_id": task_id,
            "status": "Success",
            "result": task_result.result
        }
    elif task_state == "FAILURE":
        return {"task_id": task_id, "status": "Failure", "error": str(task_result.result)}
    else:
        return {"task_id": task_id, "status": "Failure", "error": "No valid state for task."}


async def remove_task(task_id: str) -> bool:
    if task_id in all_tasks.keys():
        task_result = AsyncResult(task_id)
        task_result.revoke(terminate=True)
        del all_tasks[task_id]
        return True
    else:
        return False
