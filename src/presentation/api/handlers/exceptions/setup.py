from fastapi import FastAPI

from src.core.application.task.exceptions import TaskNotExists
from src.core.application.task.exceptions import (
    UserNotExists as TUserNoeExists,
)
from src.core.application.user.exceptions import (
    UserAlreadyExists,
    UserNotExists,
)

from . import task, user


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserNotExists, user.user_not_exists)
    app.add_exception_handler(TUserNoeExists, task.user_not_exists)
    app.add_exception_handler(TaskNotExists, task.task_not_exists)
    app.add_exception_handler(UserAlreadyExists, user.user_already_exists)
