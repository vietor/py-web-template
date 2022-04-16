from logging.config import fileConfig

from alembic import context

from core.db import engine
from core.models import BaseDBModel

config = context.config
fileConfig(config.config_file_name)

target_metadata = BaseDBModel.metadata


def run_migrations_offline():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
