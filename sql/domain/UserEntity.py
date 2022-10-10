#  Copyright (c) 2021 Vladyslav Synytsyn.
from sqlalchemy import Column, Table, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from sql.domain.Base import Base


_association_table = Table(
    'user_lessons', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('lesson_id', ForeignKey('lessons.lesson_id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)

    lessons = relationship(
        'Lesson',
        secondary=_association_table,
        backref='users'
    )
