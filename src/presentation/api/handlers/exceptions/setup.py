from fastapi import FastAPI

from src.core.application.user.exceptions import (
    UserAlreadyExists,
    UserNotExists,
)

from . import user


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserNotExists,
        user.user_not_exists,
    )
    app.add_exception_handler(
        UserAlreadyExists,
        user.user_already_exists,
    )
