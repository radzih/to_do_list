from typing import Optional, Protocol, TypeAlias

from src.core.domain import models

UserId: TypeAlias = int
TaskId: TypeAlias = int


class UserSaver(Protocol):
    async def save_user(self, user: models.User) -> UserId:
        ...


class UserReader(Protocol):
    async def read_user_by_id(self, user_id: UserId) -> Optional[models.User]:
        ...

    async def read_user_by_email(self, email: str) -> Optional[models.User]:
        ...

    async def read_users(self, offset: int, limit: int) -> list[models.User]:
        ...


class TaskSaver(Protocol):
    async def save_task(self, task: models.Task) -> TaskId:
        ...


class TaskReader(Protocol):
    async def read_task_by_id(self, task_id: TaskId) -> Optional[models.Task]:
        ...

    async def read_tasks_by_user_id(
        self,
        offset: int,
        limit: int,
        user_id: UserId,
        completed: Optional[bool],
        overdue: Optional[bool],
    ) -> list[models.Task]:
        ...


class TaskRemover(Protocol):
    async def remove_task(self, task_id: TaskId) -> Optional[TaskId]:
        ...


class Commiter(Protocol):
    async def commit():
        ...
