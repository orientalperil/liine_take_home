import pendulum
from django.conf import settings
from django.test import TestCase
from pendulum import Time

from restaurants.data import get_next_day
from restaurants.data import import_csv
from restaurants.data import parse_days
from restaurants.data import parse_hours
from restaurants.data import parse_times
from restaurants.data import time_to_minutes
from restaurants.enums import DAYS_OF_WEEK
from restaurants.models import Hours
from restaurants.models import Restaurant


class ImportTestCase(TestCase):
    def test_import(self):
        path = settings.BASE_DIR / 'restaurants' / 'restaurants.csv'
        import_csv(path)


class ParsingTestCase(TestCase):
    def test_get_next_day(self):
        assert DAYS_OF_WEEK.TUESDAY == get_next_day(DAYS_OF_WEEK.MONDAY)

    def test_parse_days(self):
        with self.assertRaises(ValueError):
            parse_days('MoSat')

        expected = [
            DAYS_OF_WEEK.MONDAY,
            DAYS_OF_WEEK.SATURDAY,
        ]
        assert expected == parse_days('Mon, Sat')

        expected = [
            DAYS_OF_WEEK.MONDAY,
            DAYS_OF_WEEK.TUESDAY,
            DAYS_OF_WEEK.WEDNESDAY,
            DAYS_OF_WEEK.THURSDAY,
            DAYS_OF_WEEK.FRIDAY,
            DAYS_OF_WEEK.SATURDAY,
        ]
        assert expected == parse_days('Mon-Fri, Sat')

        expected = [
            DAYS_OF_WEEK.MONDAY,
            DAYS_OF_WEEK.TUESDAY,
            DAYS_OF_WEEK.WEDNESDAY,
            DAYS_OF_WEEK.THURSDAY,
            DAYS_OF_WEEK.SUNDAY,
        ]
        assert expected == parse_days('Mon-Thu, Sun')

        expected = [
            DAYS_OF_WEEK.FRIDAY,
            DAYS_OF_WEEK.SATURDAY,
        ]
        assert expected == parse_days('Fri-Sat')

    def test_parse_times(self):
        with self.assertRaises(ValueError):
            parse_times('3pm')

        expected = (Time(15, 0), Time(23, 30), False)
        assert expected == parse_times('3 pm - 11:30 pm')

        expected = (Time(17, 0), Time(1, 30), True)
        assert expected == parse_times('5 pm - 1:30 am')

        expected = (Time(10, 0), Time(12, 0), False)
        assert expected == parse_times('10 am - 12 pm')

        expected = (Time(10, 0), Time(12, 30), False)
        assert expected == parse_times('10 am - 12:30 pm')

        expected = (Time(17, 0), Time(0, 0), True)
        assert expected == parse_times('5 pm - 12 am')

        expected = (Time(17, 0), Time(0, 30), True)
        assert expected == parse_times('5 pm - 12:30 am')

        expected = (Time(0, 0), Time(5, 0), False)
        assert expected == parse_times('12 am - 5 am')

        expected = (Time(10, 0), Time(0, 0), True)
        assert expected == parse_times('10 am - 12 am')

        expected = (Time(10, 0), Time(1, 30), True)
        assert expected == parse_times('10 am - 1:30 am')

        expected = (Time(0, 0), Time(0, 0), True)
        assert expected == parse_times('12 am - 12 am')

        expected = (Time(14, 0), Time(2, 30), True)
        assert expected == parse_times('2 pm - 2:30 am')

    def test_parse_hours(self):
        expected = [
            [DAYS_OF_WEEK.MONDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.TUESDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.THURSDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.FRIDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.SATURDAY, Time(11, 0), Time(22, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(11, 0), Time(22, 0)],
        ]
        assert expected == parse_hours('Mon-Sun 11:00 am - 10 pm')

        expected = [
            [DAYS_OF_WEEK.MONDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.TUESDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.THURSDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.FRIDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(11, 0), Time(22, 0)],
        ]
        assert expected == parse_hours('Mon-Fri 11 am - 12 pm / Sun 11 am - 10 pm')

        expected = [
            [DAYS_OF_WEEK.MONDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.TUESDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.THURSDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.FRIDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.SATURDAY, Time(11, 0), Time(12, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(11, 0), Time(22, 0)],
        ]
        assert expected == parse_hours('Mon-Fri, Sat 11 am - 12 pm / Sun 11 am - 10 pm')

        expected = [
            [DAYS_OF_WEEK.SATURDAY, Time(15, 0), Time(0, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(0, 0), Time(1, 30)],
        ]
        assert expected == parse_hours('Sat 3 pm - 1:30 am')

        expected = [
            [DAYS_OF_WEEK.MONDAY, Time(17, 0), Time(0, 0)],
            [DAYS_OF_WEEK.TUESDAY, Time(0, 0), Time(0, 30)],
            [DAYS_OF_WEEK.TUESDAY, Time(17, 0), Time(0, 0)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(0, 0), Time(0, 30)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(17, 0), Time(0, 0)],
            [DAYS_OF_WEEK.THURSDAY, Time(0, 0), Time(0, 30)],
            [DAYS_OF_WEEK.THURSDAY, Time(17, 0), Time(0, 0)],
            [DAYS_OF_WEEK.FRIDAY, Time(0, 0), Time(1, 30)],
            [DAYS_OF_WEEK.FRIDAY, Time(17, 0), Time(0, 0)],
            [DAYS_OF_WEEK.SATURDAY, Time(0, 0), Time(1, 30)],
            [DAYS_OF_WEEK.SATURDAY, Time(15, 0), Time(0, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(0, 0), Time(1, 30)],
            [DAYS_OF_WEEK.SUNDAY, Time(15, 0), Time(23, 30)],
        ]
        assert expected == parse_hours('Mon-Wed 5 pm - 12:30 am / Thu-Fri 5 pm - 1:30 am / Sat 3 pm - 1:30 am / Sun 3 pm - 11:30 pm')

        expected = [
            [DAYS_OF_WEEK.SUNDAY, Time(15, 0), Time(0, 0)],
            [DAYS_OF_WEEK.MONDAY, Time(0, 0), Time(3, 30)],
        ]
        assert expected == parse_hours('Sun 3 pm - 3:30 am')

        expected = [
            [DAYS_OF_WEEK.MONDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.TUESDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.WEDNESDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.THURSDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.FRIDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.SATURDAY, Time(11, 0, 0), Time(0, 0, 0)],
            [DAYS_OF_WEEK.SUNDAY, Time(11, 0, 0), Time(0, 0, 0)]
        ]
        assert expected == parse_hours('Mon-Sun 11 am - 12 am')


class RestaurantTestCase(TestCase):
    def test_query(self):
        path = settings.BASE_DIR / 'restaurants' / 'restaurants.csv'
        import_csv(path)
        r = Restaurant.objects.get(name='The Cowfish Sushi Burger Bar')
        Hours.objects.create(
            restaurant=r,
            day_of_week=DAYS_OF_WEEK.MONDAY,
            open_range=(time_to_minutes(pendulum.Time(10, 0)), time_to_minutes(pendulum.Time(10, 30))),
            datetime_range=(pendulum.DateTime(2019, 1, 1), pendulum.DateTime(2020, 1, 1)),
        )

        iso_string = '2025-04-08T17:26:17Z'
        expected = [
            'The Cowfish Sushi Burger Bar',
            'Morgan St Food Hall',
            'Garland',
            'Crawford and Son',
            'Death and Taxes',
            'Caffe Luna',
            'Bida Manda',
            'The Cheesecake Factory',
            'Tupelo Honey',
            "Player's Retreat",
            'Glenwood Grill',
            'Neomonde',
            'Page Road Grill',
            'Mez Mexican',
            'Saltbox',
            'El Rodeo',
            'Provence',
            'Bonchon',
            'Tazza Kitchen',
            'Mandolin',
            "Mami Nora's",
            'Gravy',
            'Taverna Agora',
            'Char Grill',
            'Seoul 116',
            'Whiskey Kitchen',
            'Sitti',
            'Stanbury',
            'Yard House',
            "David's Dumpling",
            'Gringo a Gogo',
            'Brewery Bhavana',
            'Dashi',
            '42nd Street Oyster Bar',
            'Top of the Hill',
            'Jose and Sons',
            'Oakleaf',
            'Second Empire'
        ]
        self.maxDiff = None
        self.assertEqual(expected, [r.name for r in Restaurant.objects.get_open_restaurants(iso_string)])

        iso_string = '2025-04-08T11:00:00Z'
        assert 'The Cowfish Sushi Burger Bar' in [r.name for r in Restaurant.objects.get_open_restaurants(iso_string)]

        iso_string = '2025-04-08T23:59:00Z'
        assert 'Caffe Luna' in [r.name for r in Restaurant.objects.get_open_restaurants(iso_string)]

        iso_string = '2019-01-07T10:15:00Z'
        dt = pendulum.parse(iso_string)
        assert dt.day_of_week.name == 'MONDAY'
        assert 'The Cowfish Sushi Burger Bar' in [r.name for r in Restaurant.objects.get_open_restaurants(iso_string)]
