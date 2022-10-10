#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Optional

from sqlalchemy.orm import Session

from sql.domain import Group
from data.repository.crud_repository import CrudRepository, ID
from data.transaction.transaction_manager import transactional


class GroupRepository(CrudRepository[Group, int]):

    def __init__(self):
        super().__init__(Group, int, 'group_id')

    def find_all_by_faculty_id(self, faculty_id: ID, session: Session) -> list[Group]:
        return session.query(Group).filter(Group.faculty_id == faculty_id).all()

    def find_all_groups_by_course_and_faculty_id_for_current_year(
            self,
            course: int, faculty_id: ID, current_year: str,
            session: Session
    ) -> list[Group]:
        return session.query(Group).filter(
            Group.course == course,
            Group.faculty_id == faculty_id,
            Group.studying_years.contains(current_year)
        ).all()

    def find_by_name_and_course_and_faculty_id_and_year(
            self,
            group_name: str, course: int, faculty_id: int, year: str,
            session: Session
    ) -> Optional[Group]:
        return session.query(Group).filter(
            Group.name == group_name,
            Group.faculty_id == faculty_id,
            Group.course == course,
            Group.studying_years.contains(year)
        ).first()
