#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Optional

from sqlalchemy.orm import Session

from data.connection.connection_handler import ConnectionHandler
from sql.domain import Lesson, DaySchedule, Group
from data.repository.crud_repository import CrudRepository, ID


current_session = ConnectionHandler().create_new_session()


class LessonRepository(CrudRepository[Lesson, int]):

    def __init__(self):
        super().__init__(Lesson, int, 'lesson_id')

    def find_all_by_group_id(self, group_id: ID, session: Session = current_session) -> list[str]:
        return (session.query(Lesson.subject_name).distinct()
                .join(Lesson.day_schedule)
                .join(DaySchedule.group)
                .filter(Group.group_id == group_id)
                .all())

    def find_by_name_and_group_id(
            self,
            subject_name: str, group_id: ID,
            session: Session = current_session
    ) -> Optional[Lesson]:
        return (session.query(Lesson)
                .join(Lesson.day_schedule)
                .join(DaySchedule.group)
                .filter(Lesson.subject_name == subject_name, Group.group_id == group_id)
                .first())
