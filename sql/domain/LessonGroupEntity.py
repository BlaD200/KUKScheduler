#  Copyright (c) 2021 Vladyslav Synytsyn.
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sql import Base


class LessonGroup(Base):
    __tablename__ = 'lesson_groups'

    lesson_group_id = Column(Integer, primary_key=True)
    classroom = Column(Integer, nullable=False)
    group_name = Column(String(20))

    lesson_id = Column(ForeignKey('lessons.lesson_id', onupdate='CASCADE', ondelete='CASCADE'))
    lesson = relationship('Lesson', back_populates='lesson_groups')

    teacher_id = Column(ForeignKey('teachers.teacher_id', onupdate='CASCADE', ondelete='RESTRICT'))
    teacher = relationship('Teacher', back_populates='lesson_groups')
