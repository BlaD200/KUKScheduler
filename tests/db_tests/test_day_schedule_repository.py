#  Copyright (c) 2022 Vladyslav Synytsyn.
from sql import create_session
from sql.domain import DaySchedule, WeekDay
from sql.repositories.day_schedule_repository import DayScheduleRepository
from tests.db_tests.base_repository_test import BaseRepositoryTest


class DayScheduleRepositoryTest(BaseRepositoryTest[DaySchedule]):

    # def __init__(self, methodName: str = ...) -> None:
    #     super().__init__(methodName)
    #     self.repository = FacultyRepository()
    #     self.inner_list = ('Faculty 1', 'Faculty 2', 'Faculty 3', 'Faculty 4', 'Faculty 5')

    @classmethod
    def setUpClass(cls):
        cls.repository: DayScheduleRepository = DayScheduleRepository()
        cls.test_ids = ()

    def setUp(self) -> None:
        with create_session() as session:
            with session.begin():
                day_schedules = []
                names_to_add = ('Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5')
                for i, name in enumerate(names_to_add):
                    day_schedule = DaySchedule(day_schedule_id=i, day_of_week=WeekDay(i + 1))
                    day_schedules.append(day_schedule)
                session.add_all(day_schedules)
                self.test_ids = tuple((d.day_schedule_id for d in day_schedules))

    def tearDown(self):
        with create_session() as session:
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
