from abc import abstractmethod
from typing import Protocol


class UseCase(Protocol):
    @abstractmethod
    async def __call__(self, data):
        pass
