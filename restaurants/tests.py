import pandas
from django.conf import settings
from django.test import TestCase
from pendulum import Time

from restaurants.data import import_csv
from restaurants.data import parse_days
from restaurants.data import parse_hours
from restaurants.data import parse_times
from restaurants.enums import DAYS_OF_WEEK


class ImportTestCase(TestCase):
    def test_parse(self):
        path = settings.BASE_DIR/'restaurants'/'restaurants.csv'
        df = import_csv(path)
        for index, row in df.iterrows():
            a = row['Restaurant Name']
            b = row['Hours']

            pass

    def test_parse_days(self):
        expected = [
            DAYS_OF_WEEK.MONDAY.value,
            DAYS_OF_WEEK.TUESDAY.value,
            DAYS_OF_WEEK.WEDNESDAY.value,
            DAYS_OF_WEEK.THURSDAY.value,
            DAYS_OF_WEEK.FRIDAY.value,
            DAYS_OF_WEEK.SATURDAY.value,
        ]
        assert expected == parse_days('Mon-Fri, Sat')

        expected = [
            DAYS_OF_WEEK.MONDAY.value,
            DAYS_OF_WEEK.TUESDAY.value,
            DAYS_OF_WEEK.WEDNESDAY.value,
            DAYS_OF_WEEK.THURSDAY.value,
            DAYS_OF_WEEK.SUNDAY.value,
        ]
        assert expected == parse_days('Mon-Thu, Sun')

        expected = [
            DAYS_OF_WEEK.FRIDAY.value,
            DAYS_OF_WEEK.SATURDAY.value,
        ]
        assert expected == parse_days('Fri-Sat')

    def test_parse_times(self):
        expected = (Time(15, 0), Time(23, 30), False)
        assert expected == parse_times('3 pm - 11:30 pm')

        # expected = [17, 0, 1, 30, True]
        # assert expected == parse_times('5 pm - 1:30 am')
        #
        # expected = [10, 0, 12, 0, False]
        # assert expected == parse_times('10 am - 12 pm')
        #
        # expected = [10, 0, 12, 30, False]
        # assert expected == parse_times('10 am - 12:30 pm')
        #
        # expected = [17, 0, 0, 0, True]
        # assert expected == parse_times('5 pm - 12 am')
        #
        # expected = [17, 0, 0, 30, True]
        # assert expected == parse_times('5 pm - 12:30 am')
        #
        # expected = [0, 0, 5, 0, False]
        # assert expected == parse_times('12 am - 5 am')
        #
        # expected = [10, 0, 0, 0, True]
        # assert expected == parse_times('10 am - 12 am')
        #
        # expected = [10, 0, 1, 30, True]
        # assert expected == parse_times('10 am - 1:30 am')
        #
        # expected = [0, 0, 0, 0, True]
        # assert expected == parse_times('12 am - 12 am')
        #
        # expected = [14, 0, 2, 30, True]
        # assert expected == parse_times('2 pm - 2:30 am')

    def test_parse_hours(self):
        # expected = [
        #     [DAYS_OF_WEEK.MONDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.TUESDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.WEDNESDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.THURSDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.FRIDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.SATURDAY.value, 11, 0, 22, 0],
        #     [DAYS_OF_WEEK.SUNDAY.value, 11, 0, 22, 0],
        # ]
        # assert expected == parse_hours('Mon-Sun 11:00 am - 10 pm')
        #
        # expected = [
        #     [DAYS_OF_WEEK.MONDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.TUESDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.WEDNESDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.THURSDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.FRIDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.SUNDAY.value, 11, 0, 22, 0],
        # ]
        # assert expected == parse_hours('Mon-Fri 11 am - 12 pm / Sun 11 am - 10 pm')
        #
        # expected = [
        #     [DAYS_OF_WEEK.MONDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.TUESDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.WEDNESDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.THURSDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.FRIDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.SATURDAY.value, 11, 0, 12, 0],
        #     [DAYS_OF_WEEK.SUNDAY.value, 11, 0, 22, 0],
        # ]
        # assert expected == parse_hours('Mon-Fri, Sat 11 am - 12 pm / Sun 11 am - 10 pm')
        #
        # expected = [
        #     [DAYS_OF_WEEK.SATURDAY.value, 15, 0, 0, 0],
        #     [DAYS_OF_WEEK.SUNDAY.value, 0, 0, 1, 30],
        # ]
        # assert expected == parse_hours('Sat 3 pm - 1:30 am')
        #
        # expected = [
        #     [DAYS_OF_WEEK.MONDAY.value, 17, 0, 0, 0],
        #     [DAYS_OF_WEEK.TUESDAY.value, 0, 0, 0, 30],
        #     [DAYS_OF_WEEK.TUESDAY.value, 17, 0, 0, 0],
        #     [DAYS_OF_WEEK.WEDNESDAY.value, 0, 0, 0, 30],
        #     [DAYS_OF_WEEK.WEDNESDAY.value, 17, 0, 0, 0],
        #     [DAYS_OF_WEEK.THURSDAY.value, 0, 0, 0, 30],
        #     [DAYS_OF_WEEK.THURSDAY.value, 17, 0, 0, 0],
        #     [DAYS_OF_WEEK.FRIDAY.value, 0, 0, 1, 30],
        #     [DAYS_OF_WEEK.FRIDAY.value, 17, 0, 0, 0],
        #     [DAYS_OF_WEEK.SATURDAY.value, 0, 0, 1, 30],
        #     [DAYS_OF_WEEK.SATURDAY.value, 15, 0, 0, 0],
        #     [DAYS_OF_WEEK.SUNDAY.value, 0, 0, 1, 30],
        #     [DAYS_OF_WEEK.SUNDAY.value, 15, 0, 23, 30],
        # ]
        # assert expected == parse_hours('Mon-Wed 5 pm - 12:30 am / Thu-Fri 5 pm - 1:30 am / Sat 3 pm - 1:30 am / Sun 3 pm - 11:30 pm')

        expected = [
            [DAYS_OF_WEEK.SUNDAY.value, Time(15, 0), Time(0, 0)],
            [DAYS_OF_WEEK.MONDAY.value, Time(0, 0), Time(3, 30)],
        ]
        assert expected == parse_hours('Sun 3 pm - 3:30 am')
