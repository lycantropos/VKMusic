import calendar
import datetime
import unittest

from vk_music.services.data_access import check_filters


class UnitTestDataAccess(unittest.TestCase):
    def setUp(self):
        self.raw_filters = dict(
            owner_id='-14',
            artist=' OK Go    ',
            title='     1000 Miles Per Hour        ',
            genre='ROCK',
            min_duration='60',
            max_duration='301',
            start_datetime=717728719,
            end_datetime=5832683395,
        )
        self.filters = dict(
            owner_id=-14,
            artist='OK Go',
            title='1000 Miles Per Hour',
            genre='Rock',
            min_duration=datetime.time(minute=1),
            max_duration=datetime.time(minute=5, second=1),
            start_datetime=datetime.datetime(1992, 9, 29, 1, 5, 19),
            end_datetime=datetime.datetime(2154, 10, 30, 21, 49, 55),
        )
        self.maxDiff = None

    def test_check_filters(self):
        check_filters(self.raw_filters)
        self.assertDictEqual(self.raw_filters, self.filters)


class UnitTestDataAccessExceptions(unittest.TestCase):
    def test_check_filters_bad_int_parameters(self):
        # owner id may be integer or string representing integer with hyphen for negative values, dash is not an option
        self.assertRaises(ValueError, check_filters, dict(owner_id='–14'))
        # classic example with typos like 1-l, o-0
        self.assertRaises(ValueError, check_filters, dict(owner_id='l40'))
        self.assertRaises(ValueError, check_filters, dict(owner_id='1o'))

    def test_check_filters_bad_time_parameters(self):
        self.assertRaises(
            ValueError, check_filters,
            dict(
                min_duration=(
                                 datetime.datetime.combine(datetime.date.min, datetime.time.min) - datetime.datetime.min
                             ).total_seconds() - 1
            )
        )
        self.assertRaises(
            ValueError, check_filters,
            dict(
                max_duration=(
                                 datetime.datetime.combine(datetime.date.min, datetime.time.max) - datetime.datetime.min
                             ).total_seconds() + 1
            )
        )
        self.assertRaises(ValueError, check_filters, dict(min_duration='01:49:57'))

    def test_check_filters_bad_datetime_parameters(self):
        self.assertRaises(
            ValueError, check_filters, dict(start_datetime=calendar.timegm(datetime.datetime.max.utctimetuple()) + 1)
        )
        self.assertRaises(
            ValueError, check_filters, dict(start_datetime=calendar.timegm(datetime.datetime.min.utctimetuple()) - 1)
        )
        self.assertRaises(TypeError, check_filters, dict(start_datetime='2154-10-30 21:49:55'))


if __name__ == '__main__':
    unittest.main()
