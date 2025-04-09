import pendulum
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.postgres.fields import RangeOperators
from django.db import models
from django.db.models import Q

from core.models import CreatedUpdatedModel
from restaurants.data import time_to_minutes
from restaurants.enums import DAYS_OF_WEEK


class RestaurantQuerySet(models.QuerySet):
    def get_open_restaurants(self, iso_string):
        dt = pendulum.parse(iso_string)
        day = dt.day_of_week.name
        minutes = time_to_minutes(dt.time())
        q_open = Q(hours__open_range__startswith__lte=minutes) & Q(Q(hours__open_range__endswith__gt=minutes) | Q(hours__open_range__upper_inf=True))
        q_datetime = Q(hours__datetime_range__startswith__lte=dt) & Q(Q(hours__datetime_range__endswith__gt=dt) | Q(hours__datetime_range__upper_inf=True))
        return self.filter(q_open, q_datetime, hours__day_of_week=day).distinct()


class Restaurant(CreatedUpdatedModel):
    name = models.CharField(max_length=200)

    objects = RestaurantQuerySet.as_manager()

    class Meta:
        ordering = ['pk']


class Hours(CreatedUpdatedModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=200, choices=DAYS_OF_WEEK)
    open_range = IntegerRangeField()
    datetime_range = DateTimeRangeField()

    class Meta:
        ordering = ['-datetime_range']
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_open_range',
                expressions=[
                    ('restaurant', RangeOperators.EQUAL),
                    ('day_of_week', RangeOperators.EQUAL),
                    ('open_range', RangeOperators.OVERLAPS),
                    ('datetime_range', RangeOperators.OVERLAPS),
                ],
            ),
        ]
