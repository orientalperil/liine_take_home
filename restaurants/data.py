import re

import pandas

from restaurants.enums import DAYS_OF_WEEK


def import_csv(path):
    df = pandas.read_csv(path)
    return df


days_mapping = {
    'Mon': DAYS_OF_WEEK.MONDAY.value,
    'Tues': DAYS_OF_WEEK.TUESDAY.value,
    'Wed': DAYS_OF_WEEK.WEDNESDAY.value,
    'Thu': DAYS_OF_WEEK.THURSDAY.value,
    'Fri': DAYS_OF_WEEK.FRIDAY.value,
    'Sat': DAYS_OF_WEEK.SATURDAY.value,
    'Sun': DAYS_OF_WEEK.SUNDAY.value,
}


def get_next_day(day):
    values = list(days_mapping.values())
    i = values.index(day)
    if i+1 <= len(values)-1:
        return values[i+1]
    elif i == len(values) - 1:
        return values[0]


def parse_days(days):
    units = [x.strip() for x in days.split(',')]
    ret = []
    for unit in units:
        pattern = r'(Mon|Tues|Wed|Thu|Fri|Sat|Sun)-?(Mon|Tues|Wed|Thu|Fri|Sat|Sun)?'
        match = re.match(pattern, unit)
        g = match.groups()
        if g[1] is None:
            ret.append(days_mapping[g[0]])
        elif len(g) == 2:
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
    g = match.groups()
    g = list(g)
    if g[1] is None:
        g[1] = '00'
    if g[4] is None:
        g[4] = '00'
    if g[2] == 'am' and g[0] == '12':
        g[0] = str(int(g[0]) - 12)
    if g[2] == 'pm' and g[0] != '12':
        g[0] = str(int(g[0]) + 12)
    if g[5] == 'am' and g[3] == '12':
        g[3] = str(int(g[3]) - 12)
    if g[5] == 'pm' and g[3] != '12':
        g[3] = str(int(g[3]) + 12)
    ret = [g[0], g[1], g[3], g[4]]
    ret = [int(x) for x in ret]
    next_day = False
    if g[5] == 'am' and (ret[2] != 0 or ret[3] != 0):
        a = ret[0] * 60 + ret[1]
        b = ret[2] * 60 + ret[3]
        if b < a:
            next_day = True
    ret.append(next_day)
    return ret


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
        times = parse_times(times)
        next_day = times.pop()

        for day in days:
            if next_day:
                this_day = times[:]
                this_day[2] = 0
                this_day[3] = 0
                next_day_times = times[:]
                next_day_times[0] = 0
                next_day_times[1] = 0
                ret.append([day] + this_day)
                ret.append([get_next_day(day)] + next_day_times)
            else:
                ret.append([day] + times)
    return ret
