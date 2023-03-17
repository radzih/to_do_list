from dataclasses import dataclass
from typing import Optional

from src.core.domain import models


@dataclass
class UserCreate:
    name: str
    email: str


@dataclass
class UserUpdate:
    user_id: models.UserId
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class User:
    id: models.UserId
    name: str
    email: str


@dataclass
class UserList:
    offset: int
    limit: int
