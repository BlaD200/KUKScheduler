#  Copyright (c) 2021 Vladyslav Synytsyn.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sql import Base


class Faculty(Base):
    __tablename__ = 'faculties'

    faculty_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False, unique=True)

    groups = relationship(
        'Group',
        back_populates='faculty',
        cascade='save-update, merge, expunge, refresh-expire',
        passive_deletes='all'
    )

    def __repr__(self) -> str:
        return f"Faculty({self.faculty_id=}, {self.name=})"
