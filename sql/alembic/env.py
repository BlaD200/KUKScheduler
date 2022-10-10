import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import MetaData


sys.path.append(os.getcwd())
print(os.getcwd())

from data.config.db_config import DatabaseConfig
# DO NOT DELETE THIS LINE as it is needed for alembic to see all table models.
# noinspection PyUnresolvedReferences
from sql.domain import *


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
config.set_main_option('sqlalchemy.url', DatabaseConfig().db_url)


# TODO move to separate class
def update_schema(db_schema_name: str):
    new_meta = MetaData(schema=db_schema_name)
    for table in Base.metadata.sorted_tables:
        table.schema = db_schema_name
        table.to_metadata(new_meta)
    Base.metadata = new_meta
    global target_metadata
    target_metadata = new_meta


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    update_schema(DatabaseConfig().db_schema_name)

    print(f"{DatabaseConfig().db_schema_name=}")
    print(f"{target_metadata.schema=}")
    print([(table.name, table.schema) for table in target_metadata.sorted_tables])

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            # Alternative: "public", to put version tables in seperate schema
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
