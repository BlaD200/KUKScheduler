#  Copyright (c) 2022 Vladyslav Synytsyn.

import json
from unittest import TestCase

from parser import parse_timetable, TimetableFile


class ParserTest(TestCase):
    def test_parse_timetable(self):
        for filename in ('../test_data/1 курс ж, пр, мв КУК', '../test_data/1 курс ж, пр, мв - 2  сем'):
            with self.subTest(filename=filename):
                with open(f'{filename}-data.json', encoding='utf-8') as expected_json:
                    timetable = parse_timetable(f'{filename}.docx')
                    timetable_expected = TimetableFile(**json.load(expected_json))
                    self.assertEqual(timetable, timetable_expected, 'Must be equals')
