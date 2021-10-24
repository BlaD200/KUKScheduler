#  Copyright (c) 2021 Vladyslav Synytsyn.
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from sql import Base


class SubjectGroup(Base):
    __tablename__ = 'subject_groups'

    subject_group_id = Column(Integer, primary_key=True)
    classroom = Column(Integer, nullable=False)
    group_name = Column(String(20))

    subject_id = Column(ForeignKey('subjects.subject_id', onupdate='CASCADE', ondelete='CASCADE'))
    subject = relationship('Subject', back_populates='subject_groups')

    teacher_id = Column(ForeignKey('teachers.teacher_id', onupdate='CASCADE', ondelete='RESTRICT'))
    teacher = relationship('Teacher', back_populates='subject_groups')
