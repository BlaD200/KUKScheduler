#  Copyright (c) 2022 Vladyslav Synytsyn.

from data.connection.tables_service import DBTablesService
from data.connection.connection_handler import ConnectionHandler

from sql.domain import *


def setup():
    ConnectionHandler()
    DBTablesService(Base).create_tables()


if __name__ == '__main__':
    setup()
