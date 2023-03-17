from sqlalchemy.ext.asyncio import AsyncSession

from src.core.application.shared import interfaces


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class Commiter(interfaces.Commiter, BaseRepository):
    async def commit(self):
        await self.session.commit()
