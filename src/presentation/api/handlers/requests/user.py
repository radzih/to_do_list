from dataclasses import dataclass
from typing import Optional


@dataclass
class UserCreate:
    name: str
    email: str


@dataclass
class UserUpdate:
    name: Optional[str] = None
    email: Optional[str] = None
