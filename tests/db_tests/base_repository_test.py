#  Copyright (c) 2022 Vladyslav Synytsyn.
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Callable
from unittest import TestCase

from sql import Base, current_session
from sql.repositories.crud_repository import CrudRepository


E = TypeVar('E', bound=Base)


class BaseRepositoryTest(TestCase, Generic[E], metaclass=ABCMeta):
    repository: CrudRepository[E, int]
    test_ids: tuple

    @staticmethod
    def transactional(method: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            with current_session.begin():
                method(*args, **kwargs, session=current_session)
                current_session.rollback()

        return wrapper

    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass

    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def tearDown(self):
        pass

    @transactional
    def test_find_all(self, session):
        entities = self.repository.find_all(session)
        self.assertEqual(len(entities), len(self.test_ids))

    @transactional
    def test_find_by_id(self, session):
        entity = self.repository.find_by_id(self.test_ids[0], session)
        self.assertIsNotNone(entity)

    @abstractmethod
    def create_new_entity(self, ent_id: int) -> E:
        pass

    @transactional
    def test_save_one(self, session):
        ent_id = self.test_ids[-1] + 1
        self.assertIsNone(self.repository.find_by_id(ent_id, session))

        new_entity = self.create_new_entity(ent_id)
        self.repository.save(new_entity, session)

        entity = self.repository.find_by_id(ent_id, session)
        self.assertIsNotNone(entity)

    @transactional
    def test_save_all(self, session):
        new_entities = []
        for i in range(self.test_ids[-1] + 1, self.test_ids[-1] + 6):
            new_entities.append(self.create_new_entity(i))
        self.repository.save_all(new_entities, session)

        entities = self.repository.find_all(session)
        self.assertEqual(len(entities), len(new_entities) + len(self.test_ids))

    @abstractmethod
    def modify_entity(self, entity: E) -> E:
        pass

    @transactional
    def test_update(self, session):
        ent_id = self.test_ids[0]
        entity_to_modify = self.repository.find_by_id(ent_id, session)
        self.assertIsNotNone(entity_to_modify)

        copy = self.modify_entity(entity_to_modify)
        self.assertNotEqual(entity_to_modify, copy)
        self.repository.save(entity_to_modify, session)

        entity = self.repository.find_by_id(ent_id, session)
        self.assertEqual(entity, entity_to_modify)

    @transactional
    def test_delete_by_id(self, session):
        ent_id = self.test_ids[0]
        res = self.repository.delete_by_id(ent_id, session)
        self.assertTrue(res)

        faculties = self.repository.find_all(session)
        self.assertEqual(len(faculties), len(self.test_ids) - 1)

    @transactional
    def test_delete_by_id_not_exist(self, session):
        non_existence_id = self.test_ids[-1] + 1
        non_existence_entity = self.repository.find_by_id(non_existence_id, session)
        all_entities = self.repository.find_all(session)
        self.assertIsNone(non_existence_entity)

        res = self.repository.delete_by_id(non_existence_id, session)
        self.assertFalse(res)

        entities = self.repository.find_all(session)
        self.assertCountEqual(all_entities, entities)

    @transactional
    def test_delete_one(self, session):
        ent_id = self.test_ids[0]
        entity_to_delete = self.repository.find_by_id(ent_id, session)
        self.assertIsNotNone(entity_to_delete)

        self.repository.delete_one(entity_to_delete, session)
        entity_deleted = self.repository.find_by_id(ent_id, session)

        self.assertIsNone(entity_deleted)

    @transactional
    def test_delete_all(self, session):
        all_entities = self.repository.find_all(session)
        self.assertIsNot(len(all_entities), 0)

        self.repository.delete_all(all_entities, session)

        empty_list = self.repository.find_all(session)
        self.assertEqual(empty_list, [])
