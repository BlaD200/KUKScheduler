#  Copyright (c) 2022 Vladyslav Synytsyn.
from sql.domain import DaySchedule
from data.repository.crud_repository import CrudRepository


class DayScheduleRepository(CrudRepository):
    def __init__(self):
        super().__init__(DaySchedule, int, 'day_schedule_id')
