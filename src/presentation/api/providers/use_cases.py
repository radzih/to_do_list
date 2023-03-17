from fastapi import Depends

from src.core.application.task.use_cases import (
    CreateTask,
    GetTask,
    ListTasks,
    RemoveTask,
    UpdateTask,
)
from src.core.application.user.use_case import (
    CreateUser,
    GetUser,
    ListUsers,
    UpdateUser,
)
from src.infrastructure.database import DBGateway
from src.presentation.api.providers.stub import Stub


def create_user(
    db_gateway: DBGateway = Depends(Stub(DBGateway)),
) -> CreateUser:
    return CreateUser(db_gateway)


def list_users(db_gateway: DBGateway = Depends(Stub(DBGateway))) -> ListUsers:
    return ListUsers(db_gateway)


def update_user(
    db_gateway: DBGateway = Depends(Stub(DBGateway)),
) -> UpdateUser:
    return UpdateUser(db_gateway)


def get_user(db_gateway: DBGateway = Depends(Stub(DBGateway))) -> GetUser:
    return GetUser(db_gateway)


def create_task(
    db_gateway: DBGateway = Depends(Stub(DBGateway)),
) -> CreateTask:
    return CreateTask(db_gateway)


def list_tasks(db_gateway: DBGateway = Depends(Stub(DBGateway))) -> ListTasks:
    return ListTasks(db_gateway)


def get_task(db_gateway: DBGateway = Depends(Stub(DBGateway))) -> GetTask:
    return GetTask(db_gateway)


def update_task(
    db_gateway: DBGateway = Depends(Stub(DBGateway)),
) -> UpdateTask:
    return UpdateTask(db_gateway)


def remove_task(
    db_gateway: DBGateway = Depends(Stub(DBGateway)),
) -> RemoveTask:
    return RemoveTask(db_gateway)
