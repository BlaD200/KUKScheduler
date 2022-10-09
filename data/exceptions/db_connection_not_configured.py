#  Copyright (c) 2022 Vladyslav Synytsyn.

class DBConnectionNotConfiguredError(Exception):
    """The error class is designed to be raised when the operation over the DB is tried to be performed,
    but there isn't any connection has been established to it yet. """

    def __init__(self, message="Connection to the database is not configured."):
        self.message = message
        super().__init__(self.message)
