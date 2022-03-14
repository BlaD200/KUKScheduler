#  Copyright (c) 2022 Vladyslav Synytsyn.


from sql.domain import Teacher
from sql.repositories.crud_repository import CrudRepository


class TeacherRepository(CrudRepository[Teacher, int]):

    def __init__(self):
        super().__init__(Teacher, int, 'teacher_id')
