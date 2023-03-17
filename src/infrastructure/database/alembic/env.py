from alembic import context
from sqlalchemy import engine_from_config, pool

from src.infrastructure.database.config import load_config
from src.infrastructure.database.db import create_connection_url
from src.infrastructure.database.models import *  # noqa: F401 F403
from src.infrastructure.database.models.base import Base

config = context.config

db = load_config()
connection_url = create_connection_url(db)

config.set_main_option(
    "sqlalchemy.url", connection_url.render_as_string(False)
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        dict(**config.get_section(config.config_ini_section)),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
