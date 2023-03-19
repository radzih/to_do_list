from fastapi import Request

from src.infrastructure.database import DBGateway


async def db_gateway(request: Request) -> DBGateway:
    return DBGateway(request.state.db_session)
