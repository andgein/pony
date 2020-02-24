import unittest

from enum import Enum, IntEnum
from pony.orm import Database, Required, db_session, select

db = Database('sqlite', ':memory:')


class Result(Enum):
    SUCCESS = 0
    FAILURE = 1
    UNKNOWN = 2


class IntResult(IntEnum):
    SUCCESS = 10
    FAILURE = 11
    UNKNOWN = 12


class Test(db.Entity):
    name = Required(str)
    result = Required(Result)
    int_result = Required(IntResult)


db.generate_mapping(create_tables=True)

with db_session:
    Test(name="one", result=Result.SUCCESS, int_result=IntResult.SUCCESS)
    Test(name="two", result=Result.FAILURE, int_result=IntResult.FAILURE)
    Test(name="three", result=Result.UNKNOWN, int_result=IntResult.UNKNOWN)


class TestEnum(unittest.TestCase):
    def test_enum_1(self):
        with db_session:
            query = select(test for test in Test if test.result == Result.SUCCESS)
            self.assertEqual(1, query.count())
            self.assertEqual(query.first().result, Result.SUCCESS)

    def test_enum_2(self):
        with db_session:
            query = select(test for test in Test)
            query = query.filter(lambda test: test.result == Result.FAILURE)
            self.assertEqual(1, query.count())
            self.assertEqual(query.first().result, Result.FAILURE)

    def test_enum_3(self):
        with db_session:
            query = select(test for test in Test)
            query = query.where('test.result == Result.UNKNOWN')
            self.assertEqual(1, query.count())
            self.assertEqual(query.first().result, Result.UNKNOWN)

    def test_enum_4(self):
        with db_session:
            query = select(test for test in Test if test.int_result == IntResult.SUCCESS)
            self.assertEqual(1, query.count())
            self.assertEqual(query.first().int_result, IntResult.SUCCESS)

    def test_enum_5(self):
        with db_session:
            query = select(test for test in Test)
            query = query.filter(lambda test: test.int_result == IntResult.FAILURE)
            self.assertEqual(1, query.count())
            self.assertEqual(query.first().int_result, IntResult.FAILURE)


if __name__ == '__main__':
    unittest.main()
