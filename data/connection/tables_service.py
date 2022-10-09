#  Copyright (c) 2022 Vladyslav Synytsyn.

from sqlalchemy import inspect
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.schema import Table

from data.connection.connection_handler import ConnectionHandler
from data.exceptions.db_connection_not_configured import DBConnectionNotConfiguredError


class DBTablesService:
    def __init__(self, declarative_base: DeclarativeMeta | None = None):
        """:param declarative_base: Base metaclass, that was used to declare entity classes.
        If the custom base class was used, it should be passed to the constructor,
        otherwise, the :class:`registry` will be used to get the base class."""
        if declarative_base is not None:
            self._declarative_base = declarative_base
        else:
            self._declarative_base = registry().generate_base()

    @staticmethod
    def get_table_names() -> list[str]:
        """Returns:
            List[str]: list of table names existing in database.
        """
        engine = ConnectionHandler().get_engine
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        # for column in inspector.get_columns(table_name):
        #     print("Column: %s" % column['name'])
        return tables

    def get_tables(self) -> list[Table]:
        """Returns:
            List[Table]: list of the tables associated with the ."""
        return self._declarative_base.metadata.sorted_tables

    def create_tables(self):
        """Creates all tables associated with the :class:`.DeclarativeMeta`. in the database."""
        if not self._declarative_base.metadata or not self._declarative_base.metadata.bind:
            raise DBConnectionNotConfiguredError()
        self._declarative_base.metadata.create_all(bind=ConnectionHandler().get_engine)

    def reflect_tables(self, schema: str | None = None):
        """Reflects all tables from the database.
        If the ``schema`` argument is provided, only tables from that schema will be reflected."""
        if not self._declarative_base.metadata or not self._declarative_base.metadata.bind:
            raise DBConnectionNotConfiguredError()
        self._declarative_base.metadata.reflect(bind=ConnectionHandler().get_engine, schema=schema)

    def drop_tables(self):
        """Deletes all tables associated with the :class:`.DeclarativeMeta`. from the database."""
        if not self._declarative_base.metadata or not self._declarative_base.metadata.bind:
            raise DBConnectionNotConfiguredError()
        self._declarative_base.metadata.drop_all(bind=ConnectionHandler().get_engine)


__all__ = ['DBTablesService']
