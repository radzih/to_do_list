from dataclasses import dataclass

from src.core.application.shared import exceptions
from src.core.domain import models


@dataclass
class UserNotExists(exceptions.ApplicationException):
    user_id: models.UserId

    @property
    def message(self) -> str:
        return f"A user with the {self.user_id} id doesn't exist"


@dataclass
class UserAlreadyExists(exceptions.ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"User with the {self.email} email already exists"
