from fastapi import FastAPI

from src.config import load_config
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
from src.infrastructure.database.db import (
    create_connection_url,
    create_sa_engine,
    create_session_factory,
)
from src.presentation.api import providers
from src.presentation.api.handlers.exceptions import include_exception_handlers
from src.presentation.api.handlers.setup import include_routers
from src.presentation.api.middlewares import include_middlewares


def create_app():
    app = FastAPI()
    config = load_config()

    connection_url = create_connection_url(config.db, async_=True)
    engine = create_sa_engine(connection_url)
    session_factory = create_session_factory(engine)

    include_routers(app)
    include_exception_handlers(app)
    bind_dependencies(app)
    include_middlewares(app, session_factory)

    return app


def bind_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[DBGateway] = providers.infrastructure.db_gateway
    app.dependency_overrides[ListUsers] = providers.use_cases.list_users

    app.dependency_overrides[CreateTask] = providers.use_cases.create_task
    app.dependency_overrides[RemoveTask] = providers.use_cases.remove_task
    app.dependency_overrides[ListTasks] = providers.use_cases.list_tasks
    app.dependency_overrides[GetTask] = providers.use_cases.get_task
    app.dependency_overrides[UpdateTask] = providers.use_cases.update_task

    app.dependency_overrides[CreateUser] = providers.use_cases.create_user
    app.dependency_overrides[GetUser] = providers.use_cases.get_user
    app.dependency_overrides[UpdateUser] = providers.use_cases.update_user


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app)
