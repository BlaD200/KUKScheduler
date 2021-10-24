# Copyright (c) 2021 Vladyslav Synytsyn.

from .docx_parser import parse_timetable
from .parser_data import TimetableFile


__all__ = [
    'parse_timetable',
    'TimetableFile'
]
