from dataclasses import asdict
from datetime import datetime
from typing import Optional

from sqlalchemy import exc, insert, select, update

from src.core.application.shared import interfaces
from src.core.domain import models
from src.infrastructure.database import models as tables
from src.infrastructure.database.repositories.base import BaseRepository


class TaskReader(interfaces.TaskReader, BaseRepository):
    async def read_task_by_id(
        self, task_id: models.TaskId
    ) -> Optional[models.Task]:
        result = await self.session.execute(
            tables.Task.__table__.select().where(tables.Task.id == task_id)
        )
        row = result.fetchone()
        return models.Task(*row) if row else None

    async def read_tasks_by_user_id(
        self,
        offset: int,
        limit: int,
        user_id: models.UserId,
        completed: Optional[bool],
        overdue: Optional[bool],
    ) -> list[models.Task]:
        statement = tables.Task.__table__.select().filter_by(user_id=user_id)

        if completed is not None:
            statement = statement.filter_by(completed=completed)

        if overdue is not None:
            now = datetime.now()
            if overdue:
                statement = statement.filter(tables.Task.due_date < now)
                # TODO: if due date set to null think about it
            else:
                statement = statement.filter(tables.Task.due_date >= now)

        statement = statement.offset(offset).limit(limit)

        result = await self.session.execute(statement)
        rows = result.fetchall()

        return [models.Task(*row) for row in rows]


class TaskSaver(interfaces.TaskSaver, BaseRepository):
    async def save_task(self, task: models.Task) -> models.TaskId:
        if not task.id:
            statement = insert(tables.Task)
        else:
            statement = update(tables.Task).where(tables.Task.id == task.id)

        statement = statement.values(
            title=task.title,
            user_id=task.user_id,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date,
        ).returning(tables.Task.id)

        try:
            result = await self.session.execute(statement)
        except exc.IntegrityError:
            return None

        return result.scalar_one()


class TaskRemover(interfaces.TaskRemover, BaseRepository):
    async def remove_task(
        self, task_id: models.TaskId
    ) -> Optional[models.TaskId]:

        task = await self.session.get(tables.Task, task_id)

        await self.session.delete(task)
