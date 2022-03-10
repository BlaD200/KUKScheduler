#  Copyright (c) 2022 Vladyslav Synytsyn.

from sql.domain import User
from sql.repositories import CrudRepository


class UserRepository(CrudRepository[User, int]):

    def __init__(self):
        super().__init__(User, int, 'user_id')
