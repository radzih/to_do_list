from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.domain import models


@dataclass
class TaskCreate:
    title: str
    user_id: models.UserId
    description: Optional[str] = None
    due_date: Optional[datetime] = None


@dataclass
class TaskUpdate:
    task_id: models.TaskId
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


@dataclass
class Task:
    id: models.TaskId
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    completed: bool
    user_id: models.UserId


@dataclass
class TaskList:
    offset: int
    limit: int
    user_id: models.UserId
    completed: Optional[bool]
    overdue: Optional[bool]


@dataclass
class TaskRemove:
    task_id: models.TaskId
