#  Copyright (c) 2022 Vladyslav Synytsyn.

from db_tests import *
from parser_tests import *
from .setup_tests import setup
from .teardown_tests import *


setup()

_all__ = [
    'FacultyRepositoryTest',
    'DayScheduleRepositoryTest',
    'MultiThreadingSessionAccessTest',
    'ParserTes'
]
