from dataclasses import dataclass
from typing import Optional, TypeAlias

UserId: TypeAlias = int


@dataclass
class User:
    id: Optional[UserId]
    name: str
    email: str

    def update(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email

    @classmethod
    def create(cls, name: str, email: str) -> "User":
        return cls(id=None, name=name, email=email)
