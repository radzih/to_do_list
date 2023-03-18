from dataclasses import asdict

from fastapi import APIRouter, Depends, Response, status

from src.core.application.task.dto import TaskList
from src.core.application.task.use_cases import ListTasks
from src.core.application.user import dto, exceptions
from src.core.application.user.use_case import (
    CreateUser,
    GetUser,
    ListUsers,
    UpdateUser,
)
from src.core.domain import models
from src.presentation.api.handlers import requests, responses
from src.presentation.api.handlers.helpers import PaginationService
from src.presentation.api.providers.stub import Stub

router = APIRouter(tags=["User"], prefix="/v1/user")

PAGE_SIZE = 10
DEFAULT_OFFSET = 0


@router.post(
    "",
    status_code=201,
    responses={
        status.HTTP_201_CREATED: {
            "model": responses.UserId,
        },
        status.HTTP_409_CONFLICT: {
            "model": responses.ErrorResult[exceptions.UserAlreadyExists]
        },
    },
)
async def create_user(
    data: requests.UserCreate,
    response: Response,
    create_user: CreateUser = Depends(Stub(CreateUser)),
) -> responses.User:
    user_id = await create_user(dto.UserCreate(**asdict(data)))
    return responses.UserId(id=user_id)


@router.patch(
    "/{user_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.UserNotExists],
        },
        status.HTTP_409_CONFLICT: {
            "model": responses.ErrorResult[exceptions.UserAlreadyExists]
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(
    response: Response,
    user_id: models.UserId,
    user_update: requests.UserUpdate,
    update_user: UpdateUser = Depends(Stub(UpdateUser)),
):
    await update_user(dto.UserUpdate(user_id, **asdict(user_update)))


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Paginated[responses.User]}
    },
)
async def list_users(
    pagination_service: PaginationService = Depends(PaginationService),
    list_users: ListUsers = Depends(Stub(ListUsers)),
):
    offset, limit = pagination_service.get_offset_limit()

    dto_users = await list_users(dto.UserList(offset, limit))
    users = [responses.User(**asdict(user)) for user in dto_users]

    return pagination_service.paginate_response(users)


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": responses.User},
        status.HTTP_404_NOT_FOUND: {
            "model": responses.ErrorResult[exceptions.UserNotExists],
        },
    },
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    response: Response,
    get_user: GetUser = Depends(Stub(GetUser)),
):
    user = await get_user(user_id)
    return user


@router.get(
    "/{user_id}/tasks",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Paginated[responses.Task]}
    },
)
async def list_user_tasks(
    user_id: models.UserId,
    overdue: bool | None = None,
    completed: bool | None = None,
    list_tasks: ListTasks = Depends(Stub(ListTasks)),
    pagination_service: PaginationService = Depends(PaginationService),
):
    offset, limit = pagination_service.get_offset_limit()

    dto_tasks = await list_tasks(
        TaskList(offset, limit, user_id, completed, overdue)
    )
    tasks = [responses.Task(**asdict(task)) for task in dto_tasks]

    return pagination_service.paginate_response(tasks)
