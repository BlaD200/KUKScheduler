#  Copyright (c) 2021 Vladyslav Synytsyn.
from sqlalchemy import Column, Table, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from sql import Base


_association_table = Table(
    'user_groups', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('group_id', ForeignKey('groups.group_id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)

    groups = relationship(
        'Group',
        secondary=_association_table,
        backref='users'
    )
