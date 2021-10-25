# Copyright (c) 2021 Vladyslav Synytsyn.
import enum

from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from sql import Base


class WeekDay(enum.Enum):
    monday = 1,
    tuesday = 2,
    wednesday = 3,
    thursday = 4,
    friday = 5,
    saturday = 6,
    sunday = 7


class DaySchedule(Base):
    __tablename__ = 'day_schedule'

    day_schedule_id = Column(Integer, primary_key=True)
    day_of_week = Column(Enum(WeekDay), nullable=False)

    group_id = Column(ForeignKey('groups.group_id', onupdate='CASCADE', ondelete='RESTRICT'))
    group = relationship('Group', back_populates='day_schedules')
    lessons = relationship(
        'Lesson',
        back_populates='day_schedule',
        cascade='save-update, merge, expunge, refresh-expire',
        passive_deletes='all'
    )

    def __repr__(self):
        return (f'DaySchedule('
                f'id={self.day_schedule_id}), '
                f'day_of_week={self.day_of_week}, group_id={self.group_id}')
