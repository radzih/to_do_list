from dataclasses import asdict
from typing import Optional

from src.core.application.shared.use_case import UseCase
from src.core.domain import models

from . import dto, exceptions, interfaces


class CreateUser(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.UserCreate) -> models.UserId:
        user = models.User.create(**asdict(data))
        user_id = await self.db_gateway.save_user(user)

        if not user_id:
            raise exceptions.UserAlreadyExists(user.email)

        await self.db_gateway.commit()

        return user_id


class GetUser(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: models.UserId) -> Optional[dto.User]:
        user = await self.db_gateway.read_user_by_id(data)

        if not user:
            raise exceptions.UserNotExists(data)

        return dto.User(**asdict(user))


class UpdateUser(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.UserUpdate) -> models.UserId:
        user = await self.db_gateway.read_user_by_id(data.user_id)

        if not user:
            raise exceptions.UserNotExists(data.user_id)

        user.update(name=data.name, email=data.email)

        user_id = await self.db_gateway.save_user(user)

        if not user_id:
            raise exceptions.UserAlreadyExists(data.email)

        await self.db_gateway.commit()

        return user_id


class ListUsers(UseCase):
    def __init__(self, db_gateway: interfaces.DBGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: dto.UserList) -> list[dto.User]:
        users = await self.db_gateway.read_users(data.offset, data.limit)
        return [dto.User(**asdict(user)) for user in users]
