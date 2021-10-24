#  Copyright (c) 2021 Vladyslav Synytsyn.

from dataclasses import dataclass


@dataclass
class LessonGroup:
    teacher: str
    classroom: int
    group: str = None


@dataclass
class Lesson:
    subject_name: str

    lesson_type: str
    lesson_slot: int
    lesson_slot_duration: str

    dates: list[str]
    lesson_groups: list[LessonGroup]


@dataclass
class DaySchedule:
    day_of_week: str
    lessons: list[Lesson]


@dataclass
class Group:
    name: str
    day_schedules: list[DaySchedule]


@dataclass
class TimetableFile:
    faculty_name: str
    course: str
    studying_years: str

    groups: list[Group]
