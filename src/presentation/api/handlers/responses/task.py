from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.domain.models import TaskId, UserId


@dataclass
class Task:
    id: TaskId
    title: str
    user_id: UserId
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False


@dataclass
class TaskId:
    id: TaskId
