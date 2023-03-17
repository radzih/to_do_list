from dataclasses import asdict
from typing import Optional

from src.core.application.shared.use_case import UseCase
from src.core.domain import models

from . import dto, exceptions, interfaces


class CreateTask(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.TaskCreate) -> models.TaskId:
        task = models.Task.create(**asdict(data))
        task_id = await self.db_gateway.save_task(task)
        if not task_id:
            raise exceptions.UserNotExists(data.user_id)
        await self.db_gateway.commit()
        return task_id


class GetTask(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: models.TaskId) -> Optional[dto.Task]:
        task = await self.db_gateway.read_task_by_id(data)

        if not task:
            raise exceptions.TaskNotExists(data)

        return dto.Task(**asdict(task))


class UpdateTask(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.TaskUpdate) -> models.TaskId:
        task = await self.db_gateway.read_task_by_id(data.task_id)

        if not task:
            raise exceptions.TaskNotExists(data.task_id)

        task.update(
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            completed=data.completed,
        )

        await self.db_gateway.save_task(task)
        await self.db_gateway.commit()

        return task.id


class ListTasks(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.TaskList) -> list[dto.Task]:
        tasks = await self.db_gateway.read_tasks_by_user_id(
            data.offset, data.limit, data.user_id, data.completed, data.overdue
        )
        return [dto.Task(**asdict(task)) for task in tasks]


class RemoveTask(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.TaskRemove):
        task = await self.db_gateway.read_task_by_id(data.task_id)

        if not task:
            raise exceptions.TaskNotExists(data.task_id)

        await self.db_gateway.remove_task(data.task_id)
        await self.db_gateway.commit()
