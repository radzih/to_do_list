from dataclasses import asdict

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException, RequestValidationError

from src.core.application.task import dto, exceptions
from src.core.application.task.use_cases import (
    CreateTask,
    GetTask,
    ListTasks,
    RemoveTask,
    UpdateTask,
)
from src.core.domain import models
from src.presentation.api.handlers import helpers, requests, responses
from src.presentation.api.handlers.helpers import PaginationService
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
    response: Response,
    create_task: CreateTask = Depends(Stub(CreateTask)),
):
    try:
        task_id = await create_task(dto.TaskCreate(**asdict(data)))
    except exceptions.UserNotExists as err:
        response.status_code = status.HTTP_404_NOT_FOUND
        return responses.ErrorResult(message=err.message, data=err)
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
    response: Response,
    update_task: UpdateTask = Depends(Stub(UpdateTask)),
):
    try:
        await update_task(dto.TaskUpdate(task_id, **asdict(data)))
    except exceptions.TaskNotExists as err:
        response.status_code = status.HTTP_404_NOT_FOUND
        return responses.ErrorResult(message=err.message, data=err)


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
    response: Response,
    task_id: int,
    get_task: GetTask = Depends(Stub(GetTask)),
):
    try:
        task = await get_task(task_id)
    except exceptions.TaskNotExists as err:
        response.status_code = status.HTTP_404_NOT_FOUND
        return responses.ErrorResult(message=err.message, data=err)
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
    response: Response,
    remove_task: RemoveTask = Depends(Stub(RemoveTask)),
):
    try:
        await remove_task(dto.TaskRemove(task_id))
    except exceptions.TaskNotExists as err:
        response.status_code = status.HTTP_404_NOT_FOUND
        return responses.ErrorResult(message=err.message, data=err)


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
    response: Response,
    update_task: UpdateTask = Depends(Stub(UpdateTask)),
) -> None:
    try:
        await update_task(
            dto.TaskUpdate(task_id, None, None, None, data.completed)
        )
    except exceptions.TaskNotExists as err:
        response.status_code = status.HTTP_404_NOT_FOUND
        return responses.ErrorResult(message=err.message, data=err)


# @router.patch("/{task_id}/incomplete")
