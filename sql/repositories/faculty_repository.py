#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Optional

from sqlalchemy.orm import Session

from sql import current_session
from sql.domain import Faculty
from sql.repositories.crud_repository import CrudRepository


class FacultyRepository(CrudRepository[Faculty, int]):

    def __init__(self):
        super().__init__(Faculty, int, 'faculty_id')

    def find_by_name(self, name: str, session: Session = current_session) -> Optional[Faculty]:
        return session.query(Faculty).filter(Faculty.name == name).first()
