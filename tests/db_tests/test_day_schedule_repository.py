#  Copyright (c) 2022 Vladyslav Synytsyn.

from data.connection.connection_handler import ConnectionHandler
from sql.domain import DaySchedule, WeekDay
from sql.repositories.day_schedule_repository import DayScheduleRepository
from tests.db_tests.abstract_repository_test import AbstractRepositoryTest


class DayScheduleRepositoryTest(AbstractRepositoryTest[DaySchedule]):

    @classmethod
    def setUpClass(cls):
        cls.repository: DayScheduleRepository = DayScheduleRepository()
        cls.test_ids = ()

    def setUp(self) -> None:
        session = ConnectionHandler().create_new_session()
        with session.begin():
            day_schedules = []
            names_to_add = ('Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5')
            for i, name in enumerate(names_to_add):
                day_schedule = DaySchedule(day_of_week=WeekDay(i + 1))
                day_schedules.append(day_schedule)
            session.add_all(day_schedules)
            self.test_ids = tuple((d.day_schedule_id for d in session.query(DaySchedule).all()))

    def tearDown(self):
        session = ConnectionHandler().create_new_session()
        with session.begin():
            for i in session.query(DaySchedule).all():
                session.delete(i)

    def create_new_entity(self, ent_id) -> DaySchedule:
        return DaySchedule(day_schedule_id=ent_id, day_of_week=WeekDay(1))

    def modify_entity(self, entity: DaySchedule) -> DaySchedule:
        day: WeekDay = entity.day_of_week
        new_day = WeekDay(day.value + 1 % len(WeekDay))
        copy = DaySchedule(day_schedule_id=entity.day_schedule_id, day_of_week=entity.day_of_week)
        entity.day_of_week = new_day
        return copy
