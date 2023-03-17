from fastapi import FastAPI

from . import task, user


def include_routers(app: FastAPI) -> None:
    app.include_router(user.router)
    app.include_router(task.router)
