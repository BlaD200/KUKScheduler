#  Copyright (c) 2022 Vladyslav Synytsyn.

from sql.domain import Lesson
from sql.repositories import CrudRepository


class LessonRepository(CrudRepository[Lesson, int]):

    def __init__(self):
        super().__init__(Lesson, int, 'lesson_id')
