#  Copyright (c) 2022 Vladyslav Synytsyn.

from sql.domain import LessonGroup
from data.repository.crud_repository import CrudRepository


class LessonGroupRepository(CrudRepository[LessonGroup, int]):

    def __init__(self):
        super().__init__(LessonGroup, int, 'lesson_group_id')
