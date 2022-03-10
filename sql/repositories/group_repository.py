#  Copyright (c) 2022 Vladyslav Synytsyn.

from sql.domain import Group
from sql.repositories import CrudRepository


class GroupRepository(CrudRepository[Group, int]):

    def __init__(self):
        super().__init__(Group, int, 'group_id')
