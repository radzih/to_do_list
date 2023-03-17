from typing import Optional

from sqlalchemy import exc, insert, update

from src.core.application.shared import interfaces
from src.core.domain import models
from src.infrastructure.database import models as tables
from src.infrastructure.database.repositories.base import BaseRepository


class UserSaver(interfaces.UserSaver, BaseRepository):
    async def save_user(self, user: models.User) -> Optional[models.UserId]:
        if not user.id:
            statement = (
                insert(tables.User)
                .values(name=user.name, email=user.email)
                .returning(tables.User.id)
            )
        else:
            statement = (
                update(tables.User)
                .where(tables.User.id == user.id)
                .values(name=user.name, email=user.email)
                .returning(tables.User.id)
            )

        try:
            result = await self.session.execute(statement)
            await self.session.flush()
        except exc.IntegrityError:
            return None

        return result.scalar_one()


class UserReader(interfaces.UserReader, BaseRepository):
    async def read_user_by_id(
        self, user_id: models.UserId
    ) -> Optional[models.User]:
        result = await self.session.execute(
            tables.User.__table__.select().where(tables.User.id == user_id)
        )
        row = result.fetchone()
        return models.User(*row) if row else None

    async def read_user_by_email(self, email: str) -> Optional[models.User]:
        result = await self.session.execute(
            tables.User.__table__.select().where(tables.User.email == email)
        )
        row = result.fetchone()
        return models.User(**row) if row else None

    async def read_users(self, offset: int, limit: int) -> list[models.User]:
        statement = tables.User.__table__.select().offset(offset).limit(limit)
        result = await self.session.execute(statement)
        rows = result.fetchall()
        return [models.User(*row) for row in rows]
