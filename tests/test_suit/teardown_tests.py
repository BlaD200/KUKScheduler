#  Copyright (c) 2022 Vladyslav Synytsyn.

from data.connection.tables_service import DBTablesService
from data.connection.connection_handler import ConnectionHandler
from data.config.db_config import DatabaseConfig
from sql.domain import *


def teardown():
    ConnectionHandler()
    db_tables_service = DBTablesService(Base)
    names = db_tables_service.get_table_names(DatabaseConfig().db_schema_name)
    print(sorted(names))
    print([table.name for table in db_tables_service.get_tables()])
    print('Dropping tables...')
    db_tables_service.drop_tables()


if __name__ == '__main__':
    teardown()
