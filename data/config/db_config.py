#  Copyright (c) 2021 Vladyslav Synytsyn.
"""This module reads environment variables related to DB to python variables."""

from os import getenv
from typing import Optional


print('INIT sql.db_config')


class DatabaseConfig:
    """Class stores database configuration info"""

    def __init__(self, /, database_url: Optional[str] = None, schema_name: Optional[str] = None):
        """
        If optional ``database_url`` param passed stores it as a url to database,
        otherwise reads configuration from the env variables.

        If ``DATABASE_ULR`` env variable is set, uses it to store the connection url,
        otherwise forming connection url from the template
        ``postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}``

        Environment variables:
            * DATABASE_URL - url, used to connect to the DB
            * DATABASE_USERNAME - name of the DB user
            * DATABASE_PASSWORD - password for the user
            * DATABASE_HOST - url, where DB is running (127.0.0.1)
            * DATABASE_PORT - port, where DB is running (5432
            * DATABASE_NAME - name of the DB to connect to
            * SCHEMA_NAME - name of the schema, tables located in
        """
        self._db_url: Optional[str] = database_url if database_url else getenv('DATABASE_URL')

        self._db_username: Optional[str] = getenv('DATABASE_USERNAME')
        self._db_password: Optional[str] = getenv('DATABASE_PASSWORD')
        self._db_host: Optional[str] = getenv('DATABASE_HOST')
        self._db_port: Optional[int] = getenv('DATABASE_PORT')
        self._db_name: Optional[str] = getenv('DATABASE_NAME')

        self._db_schema_name: Optional[str] = schema_name if schema_name else getenv('SCHEMA_NAME')

    @property
    def db_url(self) -> Optional[str]:
        """:return: connection url to the DB or None, if it cannot be formed"""

        if self._db_url:
            return self._db_url
        if all([self._db_username, self._db_password, self._db_host, self._db_port, self._db_name]):
            return f'postgresql://{self._db_username}:{self._db_password}@' \
                   f'{self._db_host}:{self._db_port}/{self._db_name}'
        return None

    @db_url.setter
    def db_url(self, url: str):
        self._db_url = url

    @property
    def db_schema_name(self):
        """Return name of the schema to use"""
        return self._db_schema_name

    @db_schema_name.setter
    def db_schema_name(self, schema_name: str):
        self._db_schema_name = schema_name
