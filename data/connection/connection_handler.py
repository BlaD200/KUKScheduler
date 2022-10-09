#  Copyright (c) 2022 Vladyslav Synytsyn.

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker, registry

from data.config.db_config import DatabaseConfig
from data.exceptions.db_connection_not_configured import DBConnectionNotConfiguredError
from sql.domain.Base import Base


print('INIT data.connection.connection_handler')


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionHandler(metaclass=SingletonMeta):
    """
    Class responsible for creating and managing connection to database.
    Configures the connection and ``Base`` for entity class declarations.
    """

    def __init__(self, /, config: DatabaseConfig = None):
        if not config:
            self._config = DatabaseConfig()
        else:
            self._config = config
        self._engine: Engine | None = None
        self.scoped_session: scoped_session | None = None
        self.configure_connection()

    def configure_connection(self):
        """Initializing connection to DB, if not yet exist,
        using config from :class:`DatabaseConfig`.
        """
        if not self._engine and self._config.db_url:
            if self._config.db_schema_name:
                self._update_schema()
                self._engine = create_engine(
                    self._config.db_url, future=True,
                    execution_options={"schema_translate_map": {None: self._config.db_schema_name}}
                )
            else:
                self._engine = create_engine(self._config.db_url, future=True)
            Base.metadata.bind = self._engine
            # logger.info('SQLAlchemy engine created')
        if not self.scoped_session:
            session_factory = sessionmaker(bind=self._engine)
            self.scoped_session = scoped_session(session_factory)

    def update_config(self, database_config: DatabaseConfig):
        """
        Applies a new configuration to database connection.

        If :class:`sqlalchemy.orm.Session` was created,
        uses new config to reconfigure the connection.

        If no session was created, will create the new one.

        :param database_config: Configuration, used to create a connection to DB
        """
        schema = self._config.db_schema_name
        self._config = database_config
        if schema != self._config.db_schema_name:
            self._engine = None
            self.scoped_session = None
        self.configure_connection()

    def create_new_session(self) -> Session:
        """Creates and returns the session object.

        .. return::
            Session: session object to performs operations in DB.

        .. note::
            If the is no information about connection config, session won't be valid,
            until appropriate configuration will be passed.
            See :meth:`ConnectionHandler.update_config`
        """
        self.scoped_session.remove()
        return self.scoped_session()

    def get_current_session(self) -> Session:
        """
        Returns:
            Session: session object to performs operations in DB.

        Note:
            If the session has been already created for the current thread - returns it,
             otherwise, creates a new one.
        """
        return self.scoped_session()

    @property
    def get_engine(self) -> Engine:
        """:returns: engine object to performs operations in DB."""
        if not self._engine:
            raise DBConnectionNotConfiguredError()
        return self._engine

    def get_database_revision(self) -> str:
        """
        Creating session if not exist.

        :return: alembic revision slug
        """
        session = self.create_new_session()
        versions = \
            Table('alembic_version', Base.metadata, autoload=True, autoload_with=self._engine)

        version: str = session.query(versions).all()[-1][0]
        session.close()
        return version

    def _update_schema(self):
        new_meta = MetaData(schema=self._config.db_schema_name)
        for table in Base.metadata.sorted_tables:
            table.schema = self._config.db_schema_name
            table.to_metadata(new_meta)

        Base.metadata = new_meta
        mapper_registry = registry()
        mapper_registry.metadata = new_meta


# Base: DeclarativeMeta = declarative_base()
# Base.metadata = MetaData()

# mapper_registry = registry()
#
# Base = mapper_registry.generate_base()

# if __name__ == "__main__":
#     # The client code.
#
#     from sql.db_config import DatabaseConfig
#
#     config = DatabaseConfig(schema_name='test_name')
#     s1 = ConnectionHandler(config=config)
#     s2 = ConnectionHandler()
#
#     if id(s1) == id(s2):
#         print("Singleton works, both variables contain the same instance.")
#         print(f'{s1.config().db_schema_name=}')
#         print(f'{s2.config().db_schema_name=}')
#     else:
#         print("Singleton failed, variables contain different instances.")

__all__ = ['ConnectionHandler']
