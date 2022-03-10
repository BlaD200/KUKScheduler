#  Copyright (c) 2022 Vladyslav Synytsyn.
import unittest

from tests.db_tests.test_day_schedule_repository import DayScheduleRepositoryTest
from tests.db_tests.test_faculty_repository import FacultyRepositoryTest


def create_test_suite():
    testCases = []
    testCases.append(FacultyRepositoryTest)
    testCases.append(DayScheduleRepositoryTest)

    test_loader = unittest.TestLoader()
    # module_tests = test_loader.loadTestsFromModule(db_tests.test_faculty_repository)
    # print(module_tests.countTestCases(), module_tests)

    suites = []
    for tc in testCases:
        suites.append(test_loader.loadTestsFromTestCase(tc))

    return unittest.TestSuite(suites)


def run_db_test():
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_db_test()
