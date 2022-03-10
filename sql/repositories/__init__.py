#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Optional, Generic, TypeVar

from sqlalchemy.orm import Session

from sql import Base


E = TypeVar('E', bound=Base)
ID = TypeVar('ID')


class CrudRepository(Generic[E, ID]):

    def __init__(self, entity: E, pk_type: ID, pk_name):
        self.__entity = entity
        self.__pk_type = pk_type
        self.__pk_name = pk_name

    def find_all(self, session: Session) -> list[E]:
        return session.query(self.__entity).all()

    def find_by_id(self, entity_id: ID, session: Session) -> Optional[E]:
        return session.query(self.__entity).filter(self.__entity.__dict__[self.__pk_name] == entity_id).first()

    def save(self, entity: E, session: Session):
        session.add(entity)

    def save_all(self, entities: list[E], session: Session):
        session.add_all(entities)

    def delete_by_id(self, entity_id: ID, session: Session) -> bool:
        if entity := self.find_by_id(entity_id, session):
            session.delete(entity)
            return True
        return False

    def delete_one(self, entity: E, session: Session):
        session.delete(entity)

    def delete_all(self, entities: list[E], session: Session):
        for entity in entities:
            self.delete_one(entity, session)
