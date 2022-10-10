#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Optional

from sqlalchemy.orm import Session

from sql.domain import Faculty, Group
from data.repository.crud_repository import CrudRepository, ID
from data.transaction.transaction_manager import transactional


class FacultyRepository(CrudRepository[Faculty, int]):

    def __init__(self):
        super().__init__(Faculty, int, 'faculty_id')

    def find_by_name(self, name: str, /, session: Session) -> Optional[Faculty]:
        return session.query(Faculty).filter(Faculty.name == name).first()

    def find_all_course_numbers_by_faculty_name_for_current_year(
            self,
            faculty_name: str, current_year: str, /,
            session: Session
    ) -> Optional[tuple[int]]:
        faculty = self.find_by_name(faculty_name, session)
        if not faculty:
            return None
        course_numbers = []
        group: Group
        for group in faculty.groups:
            if current_year in group.studying_years:
                course_numbers.append(group.course)

        return tuple(course_numbers)
