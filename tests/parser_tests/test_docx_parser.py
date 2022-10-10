#  Copyright (c) 2022 Vladyslav Synytsyn.

import json
import os
import pathlib
from unittest import TestCase

from parser import parse_timetable, TimetableFile


class ParserTest(TestCase):
    def test_parse_timetable(self):
        cwd = pathlib.Path(os.getcwd())
        test_data_path = cwd.joinpath('test_data')
        for filename in ('1 курс ж, пр, мв КУК', '1 курс ж, пр, мв - 2  сем'):
            filepath = test_data_path.joinpath(filename)
            with self.subTest(filename=filename):
                with open(f'{filepath.resolve()}-data.json', encoding='utf-8') as expected_json:
                    timetable = parse_timetable(f'{filepath.resolve()}.docx')
                    timetable_expected = TimetableFile(**json.load(expected_json))
                    self.assertEqual(timetable, timetable_expected, 'Must be equals')
