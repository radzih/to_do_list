from dataclasses import dataclass

from src.core.application.shared import exceptions
from src.core.domain.models import TaskId, UserId


@dataclass
class TaskNotExists(exceptions.ApplicationException):
    task_id: TaskId

    @property
    def message(self) -> str:
        return f"Task with id {self.task_id} doesn't exist"


@dataclass
class UserNotExists(exceptions.ApplicationException):
    user_id: UserId

    @property
    def message(self) -> str:
        return f"User with id {self.user_id} doesn't exist"
