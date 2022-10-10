#  Copyright (c) 2022 Vladyslav Synytsyn.

from data.connection.connection_handler import ConnectionHandler
from sql.domain import Faculty
from sql.repositories.faculty_repository import FacultyRepository
from tests.db_tests.abstract_repository_test import AbstractRepositoryTest


class FacultyRepositoryTest(AbstractRepositoryTest[Faculty]):

    @classmethod
    def setUpClass(cls):
        cls.repository: FacultyRepository = FacultyRepository()
        cls.test_ids = ()

    def setUp(self) -> None:
        current_session = ConnectionHandler().create_new_session()
        with current_session.begin():
            faculties = []
            names_to_add = ('Faculty 1', 'Faculty 2', 'Faculty 3', 'Faculty 4', 'Faculty 5')
            for i, name in enumerate(names_to_add):
                faculty = Faculty(name=name)
                faculties.append(faculty)
            current_session.add_all(faculties)
            # current_session.commit()
            self.test_ids = tuple((f.faculty_id for f in current_session.query(Faculty).all()))

    def tearDown(self):
        current_session = ConnectionHandler().create_new_session()
        with current_session.begin():
            for i in current_session.query(Faculty).all():
                current_session.delete(i)

    def create_new_entity(self, ent_id) -> Faculty:
        return Faculty(faculty_id=ent_id, name=f'test faculty {ent_id}')

    def modify_entity(self, entity: Faculty) -> Faculty:
        copy = Faculty(faculty_id=entity.faculty_id, name=entity.name)
        entity.name = 'new test name'
        return copy

    @AbstractRepositoryTest.transactional
    def test_find_by_name(self, session):
        test_name = 'test faculty'
        self.repository.save(Faculty(name=test_name), session)

        faculty = self.repository.find_by_name(test_name, session)
        self.assertIsNotNone(faculty)
        self.assertEqual(faculty.name, test_name)
