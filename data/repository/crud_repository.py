#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import TypeVar, Generic, Optional

from sqlalchemy.orm import Session

from sqlalchemy.orm.decl_api import DeclarativeMeta


Entity = TypeVar('Entity', bound=DeclarativeMeta)
ID = TypeVar('ID')


class CrudRepository(Generic[Entity, ID]):

    def __init__(self, entity: Entity, pk_type: ID, pk_name):
        self.__entity = entity
        self.__pk_type = pk_type
        self.__pk_name = pk_name

    def find_all(self, session: Session) -> list[Entity]:
        return session.query(self.__entity).all()

    def find_by_id(self, entity_id: ID, session: Session) -> Optional[Entity]:
        return session.query(self.__entity) \
            .filter(self.__entity.__dict__[self.__pk_name] == entity_id).first()

    def save(self, entity: Entity, session: Session):
        session.add(entity)

    def save_all(self, entities: list[Entity], session: Session):
        session.add_all(entities)

    def delete_by_id(self, entity_id: ID, session: Session) -> bool:
        if entity := self.find_by_id(entity_id, session):
            session.delete(entity)
            return True
        return False

    def delete_one(self, entity: Entity, session: Session):
        session.delete(entity)

    def delete_all(self, entities: list[Entity], session: Session):
        for entity in entities:
            self.delete_one(entity, session)
