from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

from .db_session import DatabaseSessionMiddleware


def include_middlewares(
    app: FastAPI, session_factory: async_sessionmaker
) -> None:
    app.add_middleware(
        DatabaseSessionMiddleware, session_factory=session_factory
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=("*",),
        allow_methods=("*",),
        allow_headers=("*",),
    )
