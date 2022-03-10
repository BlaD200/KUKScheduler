#  Copyright (c) 2021 Vladyslav Synytsyn.
import enum

from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from sql import Base


class LessonType(enum.Enum):
    lecture = 1,
    practice = 2


class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True)
    subject_name = Column(String(100), nullable=False)
    lesson_type = Column(Enum(LessonType), nullable=False)
    lesson_slot = Column(Integer, nullable=False)
    lesson_slot_duration = Column(String(15), nullable=False)
    lesson_dates = Column(postgresql.ARRAY(Date), nullable=False)

    day_schedule_id = Column(ForeignKey('day_schedule.day_schedule_id', onupdate='CASCADE', ondelete='RESTRICT'))
    day_schedule = relationship('DaySchedule', back_populates='lessons')

    lesson_groups = relationship(
        'LessonGroup',
        back_populates='lesson',
        cascade='all, delete, delete-orphan'
    )
