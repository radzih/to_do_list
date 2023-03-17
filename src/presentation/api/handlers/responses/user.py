from dataclasses import dataclass

from src.core.domain import models


@dataclass
class User:
    id: models.UserId
    name: str
    email: str


@dataclass
class UserId:
    id: models.UserId
