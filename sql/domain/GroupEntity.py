#  Copyright (c) 2021 Vladyslav Synytsyn.

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sql.domain.Base import Base


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    course = Column(Integer, nullable=False)
    studying_years = Column(String(10), nullable=False)

    faculty_id = Column(ForeignKey('faculties.faculty_id', onupdate='CASCADE', ondelete='RESTRICT'))
    faculty = relationship('Faculty', back_populates='groups')
    day_schedules = relationship(
        'DaySchedule',
        back_populates='group',
        cascade='save-update, merge, expunge, refresh-expire',
        passive_deletes='all'
    )

    def __repr__(self) -> str:
        return (f'Group('
                f'id={self.group_id}, '
                f'name={self.name=}, course={self.course}, years={self.studying_years}, '
                f'faculty={self.faculty_id})')
