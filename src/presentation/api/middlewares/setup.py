from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from .db_session import DatabaseSessionMiddleware


def include_middlewares(
    app: FastAPI, session_factory: async_sessionmaker
) -> None:
    app.add_middleware(
        DatabaseSessionMiddleware, session_factory=session_factory
    )
