from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeAlias

from src.core.domain.models.user import UserId

TaskId: TypeAlias = int


@dataclass
class Task:
    id: Optional[TaskId]
    title: str
    user_id: UserId
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        completed: Optional[bool] = None,
    ) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if completed is not None:
            self.completed = completed

    @classmethod
    def create(
        cls,
        title: str,
        description: Optional[str],
        due_date: Optional[datetime],
        user_id: UserId,
    ) -> "Task":
        return cls(
            id=None,
            title=title,
            description=description,
            due_date=due_date,
            user_id=user_id,
            completed=False,
        )
