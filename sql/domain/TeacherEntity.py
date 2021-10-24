#  Copyright (c) 2021 Vladyslav Synytsyn.
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sql import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    subject_groups = relationship(
        'SubjectGroup',
        back_populates='teacher',
        cascade='save-update, merge, expunge, refresh-expire',
        passive_deletes='all'
    )
