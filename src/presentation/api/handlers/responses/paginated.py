from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

Model = TypeVar("Model", bound=BaseModel, covariant=True)


class Paginated(GenericModel, Generic[Model]):
    next: str | None
    previous: str | None
    data: list[Model]
