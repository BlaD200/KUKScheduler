#  Copyright (c) 2021 Vladyslav Synytsyn.

from typing import Optional

from pydantic import BaseModel


# @dataclass(frozen=True, order=True)
class LessonGroup(BaseModel):
    teacher: str
    classroom: Optional[int]
    group: str = None


# @dataclass(frozen=True, order=True)
class Lesson(BaseModel):
    subject_name: str

    lesson_type: str
    lesson_slot: int
    lesson_slot_duration: str

    dates: list[str]
    lesson_groups: list[LessonGroup]


# @dataclass(frozen=True, order=True)
class DaySchedule(BaseModel):
    day_of_week: str
    lessons: list[Lesson]


# @dataclass(frozen=True, order=True)
class Group(BaseModel):
    name: str
    day_schedules: list[DaySchedule]


# @dataclass(frozen=True, order=True)
class TimetableFile(BaseModel):
    faculty_name: str
    course: str
    studying_years: str

    groups: list[Group]

    # def to_json(self):
    #     attr_str_list = []
    #     for attr, val in self.__dict__.items():
    #         if hasattr(val, 'to_json'):
    #             attr_str_list.append(f'{attr}: {val.to_json()}')
    #         elif isinstance(val, list):
