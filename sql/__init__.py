#  Copyright (c) 2021 Vladyslav Synytsyn.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session, declarative_base, DeclarativeMeta
from sqlalchemy.schema import Table

from sql.config import *


sqlalchemy_url = db_url if db_url is not None \
    else f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

Base: DeclarativeMeta = declarative_base()

_engine = None
_Session = None
_session = None


def create_session() -> Session:
    """
    Initializing connection to DB, if not yet exist.
    Creates and returns the session object.

    Returns:
        Session: session object to performs operations in DB.
    """
    global _engine, _Session, _session
    if _engine is None:
        _engine = create_engine(sqlalchemy_url, future=True)
        # logger.info('SQLAlchemy engine created')
    if _Session is None:
        _Session = scoped_session(sessionmaker(_engine))
        # logger.info('Scoped session created')

    if _session is None:
        _session = _Session()
    else:
        _session.close()
        # logger.debug(f'The session was closed before creating a new one: {_session}.')
        _session = _Session()
    # logger.debug(f'A new session was created: {_session}.')
    return _session


def get_tables() -> list[str]:
    """
    Creating session if not exist.

    Returns:
        List[str]: list of table names existing in database.
    """
    create_session()

    from sqlalchemy import inspect
    inspector = inspect(_engine)

    tables = [table_name for table_name in inspector.get_table_names()]
    # for column in inspector.get_columns(table_name):
    #     print("Column: %s" % column['name'])
    return tables


def get_database_revision() -> str:
    """
    Creating session if not exist.

    :return: alembic revision slug
    """
    session = create_session()
    versions = Table('alembic_version', Base.metadata, autoload=True, autoload_with=_engine)

    version: str = session.query(versions).all()[-1][0]
    session.close()
    return version


__all__ = [
    'create_session',
    'get_tables',
    'get_database_revision',
    'Base',
    'sqlalchemy_url'
]
