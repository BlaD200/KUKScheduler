#  Copyright (c) 2021 Vladyslav Synytsyn.
"""This module reads environment variables related to DB to python variables."""

from os import getenv


# Can be used for local dev db
db_username = getenv('DATABASE_USERNAME')
db_password = getenv('DATABASE_PASSWORD')
db_host = getenv('DATABASE_HOST')
db_port = getenv('DATABASE_PORT')
db_name = getenv('DATABASE_NAME')

# DATABASE_URL is set in production env
db_url = getenv('DATABASE_URL')
