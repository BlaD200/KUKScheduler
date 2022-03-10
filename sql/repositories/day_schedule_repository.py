#  Copyright (c) 2022 Vladyslav Synytsyn.
from sql.domain import DaySchedule
from sql.repositories import CrudRepository


class DayScheduleRepository(CrudRepository):
    def __init__(self):
        super().__init__(DaySchedule, int, 'day_schedule_id')
