#  Copyright (c) 2022 Vladyslav Synytsyn.

from sql import create_session
from sql.domain import Faculty
from sql.repositories.faculty_repository import FacultyRepository
from tests.db_tests import AbstractTest


class FacultyRepositoryTest(AbstractTest.BaseRepositoryTest[Faculty]):

    # def __init__(self, methodName: str = ...) -> None:
    #     super().__init__(methodName)
    #     self.repository = FacultyRepository()
    #     self.inner_list = ('Faculty 1', 'Faculty 2', 'Faculty 3', 'Faculty 4', 'Faculty 5')

    @classmethod
    def setUpClass(cls):
        cls.repository: FacultyRepository = FacultyRepository()
        cls.test_ids = ()

    def setUp(self) -> None:
        with create_session() as session:
            with session.begin():
                faculties = []
                names_to_add = ('Faculty 1', 'Faculty 2', 'Faculty 3', 'Faculty 4', 'Faculty 5')
                for i, name in enumerate(names_to_add):
                    faculty = Faculty(faculty_id=i, name=name)
                    faculties.append(faculty)
                session.add_all(faculties)
                self.test_ids = tuple((f.faculty_id for f in faculties))

    def tearDown(self):
        with create_session() as session:
            with session.begin():
                for i in session.query(Faculty).all():
                    session.delete(i)

    def create_new_entity(self, ent_id) -> Faculty:
        return Faculty(faculty_id=ent_id, name=f'test faculty {ent_id}')

    def modify_entity(self, entity: Faculty) -> Faculty:
        copy = Faculty(faculty_id=entity.faculty_id, name=entity.name)
        entity.name = 'new test name'
        return copy

    @AbstractTest.BaseRepositoryTest.transactional
    def test_find_by_name(self, session):
        test_name = 'test faculty'
        self.repository.save(Faculty(name=test_name), session)

        faculty = self.repository.find_by_name(test_name, session)
        self.assertIsNotNone(faculty)
        self.assertEqual(faculty.name, test_name)
