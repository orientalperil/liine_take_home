import itertools
import re

import pandas
import pendulum
from django.apps import apps

from restaurants.enums import DAYS_OF_WEEK


def import_csv(path):
    Hours = apps.get_model('restaurants', 'Hours')
    Restaurant = apps.get_model('restaurants', 'Restaurant')
    df = pandas.read_csv(path)
    for index, row in df.iterrows():
        restaurant = Restaurant.objects.create(name=row['Restaurant Name'])
        datetime_start = pendulum.DateTime(2020, 1, 1)
        for day, start, end in parse_hours(row['Hours']):
            start_minutes = time_to_minutes(start)
            end_minutes = time_to_minutes(end)
            # Open to 12 am next day is the same as the end of the current day so set range without upper bound
            if end_minutes == 0:
                end_minutes = None
            Hours.objects.create(
                restaurant=restaurant,
                day_of_week=day,
                open_range=(start_minutes, end_minutes),
                datetime_range=(datetime_start, None),
            )


days_mapping = {
    'Mon': DAYS_OF_WEEK.MONDAY,
    'Tues': DAYS_OF_WEEK.TUESDAY,
    'Wed': DAYS_OF_WEEK.WEDNESDAY,
    'Thu': DAYS_OF_WEEK.THURSDAY,
    'Fri': DAYS_OF_WEEK.FRIDAY,
    'Sat': DAYS_OF_WEEK.SATURDAY,
    'Sun': DAYS_OF_WEEK.SUNDAY,
}


def get_next_day(day):
    cycler = itertools.cycle(days_mapping.values())
    while next(cycler) != day:
        pass
    return next(cycler)


def parse_days(days):
    units = [x.strip() for x in days.split(',')]
    ret = []
    for unit in units:
        pattern = r'(Mon|Tues|Wed|Thu|Fri|Sat|Sun)-?(Mon|Tues|Wed|Thu|Fri|Sat|Sun)?'
        match = re.match(pattern, unit)
        if match is None:
            raise ValueError(f'{days} does not fit the pattern')
        g = match.groups()
        if g[1] is None:
            ret.append(days_mapping[g[0]])
        elif len(g) == 2:
            # Get the days in the range
            keys = list(days_mapping.keys())
            i = keys.index(g[0])
            j = keys.index(g[1])
            while i <= j:
                ret.append(days_mapping[keys[i]])
                i += 1
    return ret


def parse_times(times):
    pattern = r'(\d{1,2}):?(\d{2})? (am|pm) - (\d{1,2}):?(\d{2})? (am|pm)'
    match = re.match(pattern, times)
    if match is None:
        raise ValueError(f'{times} does not fit the pattern')
    g = match.groups()
    g = list(g)
    if g[1] is None:
        g[1] = '00'
    if g[4] is None:
        g[4] = '00'

    start = f'{g[0]}:{g[1]} {g[2]}'
    start = pendulum.parse(start, strict=False).time()
    end = f'{g[3]}:{g[4]} {g[5]}'
    end = pendulum.parse(end, strict=False).time()

    next_day = False
    if end <= start:
        next_day = True

    return start, end, next_day


def parse_hours(hours_text):
    units = [x.strip() for x in hours_text.split('/')]
    ret = []
    for unit in units:
        for i, char in enumerate(unit):
            if char.isdigit():
                break

        days = unit[:i].strip()
        days = parse_days(days)

        times = unit[i:].strip()
        start, end, next_day = parse_times(times)

        for day in days:
            if next_day:
                zero = pendulum.Time(hour=0, minute=0)
                ret.append([day, start, zero])
                # Don't add the next day if the range does not extend past midnight
                if end != zero:
                    ret.append([get_next_day(day), zero, end])
            else:
                ret.append([day, start, end])
    return ret


def time_to_minutes(time):
    return time.hour * 60 + time.minute
