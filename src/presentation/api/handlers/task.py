from dataclasses import asdict

from fastapi import APIRouter, Depends, status

from src.core.application.task import dto, exceptions
from src.core.application.task.use_cases import (
    CreateTask,
    GetTask,
    RemoveTask,
    UpdateTask,
)
from src.core.domain import models
from src.presentation.api.handlers import requests, responses
from src.presentation.api.providers.stub import Stub

router = APIRouter(prefix="/v1/task")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.TaskId},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.UserNotExists]
        },
    },
)
async def create_task(
    data: requests.TaskCreate,
    create_task: CreateTask = Depends(Stub(CreateTask)),
):
    task_id = await create_task(dto.TaskCreate(**asdict(data)))
    return responses.TaskId(task_id)


@router.patch(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.TaskNotExists]
        },
    },
)
async def update_task(
    task_id: models.TaskId,
    data: requests.TaskUpdate,
    update_task: UpdateTask = Depends(Stub(UpdateTask)),
):
    await update_task(dto.TaskUpdate(task_id, **asdict(data)))


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Task},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.TaskNotExists]
        },
    },
)
async def get_task(
    task_id: int,
    get_task: GetTask = Depends(Stub(GetTask)),
):
    task = await get_task(task_id)
    return responses.Task(**asdict(task))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.TaskNotExists]
        },
    },
)
async def delete_task(
    task_id: models.TaskId,
    remove_task: RemoveTask = Depends(Stub(RemoveTask)),
):
    await remove_task(dto.TaskRemove(task_id))


@router.patch(
    "/{task_id}/set_completed",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.TaskNotExists]
        },
    },
)
async def set_completed(
    task_id: models.TaskId,
    data: requests.TaskSetCompleted,
    update_task: UpdateTask = Depends(Stub(UpdateTask)),
) -> None:
    await update_task(
        dto.TaskUpdate(task_id, None, None, None, data.completed)
    )


