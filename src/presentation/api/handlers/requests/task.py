from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.domain.models import UserId


@dataclass
class TaskCreate:
    title: str
    user_id: UserId
    description: Optional[str] = None
    due_date: Optional[datetime] = None


@dataclass
class TaskUpdate:
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None


@dataclass
class TaskSetCompleted:
    completed: bool
