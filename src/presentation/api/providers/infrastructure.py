from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import DBGateway
from src.presentation.api.providers.stub import Stub


def db_gateway(
    session: AsyncSession = Depends(Stub(AsyncSession)),
) -> DBGateway:
    return DBGateway(session)
