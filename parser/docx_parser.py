# Copyright (c) 2021 Vladyslav Synytsyn.

import re
from dataclasses import dataclass

from docx import Document as CreateDocument
from docx.document import Document
from docx.table import Table


_teacher_regex = re.compile(
    r'(?P<teacher>'
    r'((([Дд]оц(ент)?\.? ?(з/н)?)|((ст\.)?[Вв]икл)|([Пп]роф)|[А-ЯІЇ][а-яії]{4,}) ?\.? ?'
    r'([ \w\-.а-яА-ЯіїІЇ])+?\.\10?.))')
_classroom_regex = re.compile(r'ауд.\s?(?P<classroom>\d+)')
_group_regex = re.compile(r'(?P<group>група\s*\d)(.*)?')
_date_regex = re.compile(r'(?P<date>\d{1,2}\.\d{1,2})\s?\(?(?P<classroom>\d{3})?')
_faculty_regex = re.compile(r'(?P<faculty>факультет\s*[а-яії ]*)', re.IGNORECASE)
_course_regex = re.compile(r'(?P<course>[\wі]+)\s?курс', re.IGNORECASE)
_year_regex = re.compile(
    r'((?P<semester>[\wі]+)\s?семестр)?\s*(?P<year_start>[\d]+)\s?[-–—]?\s?(?P<year_end>[\d]+)\s?н\.?р\.?',
    re.IGNORECASE
)


@dataclass
class LessonGroupClassroom:
    teacher: str
    classroom: int
    group: str = None


@dataclass
class Lesson:
    lesson_slot: int
    lesson_slot_duration: str

    subject_name: str
    lesson_type: str
    dates: list[str]
    lesson_group_classrooms: list[LessonGroupClassroom]


@dataclass
class GroupDay:
    group_name: str
    day: str
    lessons: list[Lesson]


def extract_edu_program_info(docx: Document):
    faculty: str | None = None
    course: str | None = None
    semester: str | None = None
    year_start: int | None = None
    year_end: int | None = None

    for i, p in enumerate(docx.paragraphs):
        print(i, p.text)
        if faculty_match := re.search(_faculty_regex, p.text):
            faculty = faculty_match.group("faculty")
        if course_match := re.search(_course_regex, p.text):
            course = course_match.group("course")
        if year_match := re.search(_year_regex, p.text):
            semester = year_match.group("semester")
            year_start = int(year_match.group("year_start")) if year_match.group("year_start") else None
            year_end = int(year_match.group("year_end")) if year_match.group("year_end") else None

        if faculty and course and year_start and year_end:
            break
    return faculty, course, semester, '%d-%d' % (year_start, year_end)


def extract_tables_data_from_file(tables: list[Table]) -> list[list[list[str]]]:
    data_tables = []
    # table: Table
    for table in tables:
        df = [
            ['' for _ in range(len(table.columns))] for _ in range(len(table.rows))
        ]
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                if cell.text.strip():
                    df[i][j] = cell.text.strip()  # '{:^15}'.format(cell.text.strip().split('\n')[0][:15])
                else:
                    df[i][j] = '{:^15}'.format('')
                # rels = cell.part.rels
                # for rel in cell.part.related_parts:
                #     if rels[rel].reltype == RELATIONSHIP_TYPE.HYPERLINK:
                #         # pass
                #         df[i][j] += rels[rel]._target
        data_tables.append(df)
    return data_tables


def extract_group_classroom_teacher(text: str, group: str = None) -> LessonGroupClassroom:
    teacher_match = re.search(_teacher_regex, text)
    teacher = teacher_match.group("teacher")

    classroom_match = re.search(_classroom_regex, text)
    if classroom_match:
        classroom = int(classroom_match.group("classroom"))
    else:
        classroom = None

    return LessonGroupClassroom(teacher, classroom, group)


def extract_dates(text: str) -> list[str]:
    return [
        x.group('date') + (x.group('classroom') if x.group('classroom') else '')
        for x in re.finditer(_date_regex, text)
    ]


def parse_timetable():
    docx = CreateDocument('../test_data/1 курс ж, пр, мв КУК.docx')
    data_tables = extract_tables_data_from_file(docx.tables)

    faculty, course, semester, studying_years = extract_edu_program_info(docx)

    for i, table in enumerate(data_tables[:]):
        print('День ', i + 1)
        print('-' * (40 * 2 + 10 * 2 + 10))

        day = 'День %d' % (i + 1)
        group_name = table[0][2]
        lessons: list[Lesson] = []
        group_day = GroupDay(day=day, group_name=group_name, lessons=lessons)

        for row in table[1:]:
            lesson_slot = int(row[0])
            lesson_slot_duration = row[1]

            for j, cell in enumerate(row[:3]):
                if j > 2:
                    #     print('{:^10}'.format(''.join(cell.split('\n')[:3])), end=' | ')
                    # else:
                    #     print('{:^40}'.format(' '.join(cell.split('\n')[:3])), end=' | ')
                    if cell.strip():
                        group_classrooms = []
                        group_matchers = list(re.finditer(_group_regex, cell))
                        if group_matchers:
                            for group_match in group_matchers:
                                group = group_match.group('group')
                                group_srt = group_match.group()
                                group_classroom = extract_group_classroom_teacher(group_srt, group)
                                group_classrooms.append(group_classroom)
                        else:
                            group_classroom = extract_group_classroom_teacher(cell)
                            group_classrooms.append(group_classroom)

                        lines = cell.split('\n')
                        subject_name = lines[0]
                        lesson_type = lines[1].split(',')[0].split()[0]
                        dates = extract_dates(cell)
                        lesson = Lesson(
                            lesson_slot, lesson_slot_duration,
                            subject_name, lesson_type, dates,
                            group_classrooms
                        )

                        if lesson not in lessons:
                            lessons.append(lesson)

            print('\n', '-' * (40 * 2 + 10 * 2 + 10))
        # print(*[x[:4] for x in table], sep='\n')
        print()

        print(group_day.group_name, group_day.day)
        for lesson in group_day.lessons:
            print(lesson.subject_name, ' | ', lesson.lesson_type, lesson.dates, ' | ', lesson.lesson_group_classrooms)
        print()

        # Назва
        # Дати (Аудиотрія) дати
        # (Зум) .part.rels[].reltype == RT.HYPERLINK ? : rels[rel]._target
        # Викладач
        # (Зум)
        # Аудиторія (Optional)
        #


if __name__ == '__main__':
    parse_timetable()
