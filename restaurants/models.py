from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, IntegerRangeField
from django.contrib.postgres.fields import RangeOperators
from django.db import models

from core.models import CreatedUpdatedModel
from restaurants.enums import DAYS_OF_WEEK


class Restaurant(CreatedUpdatedModel):
    name = models.CharField(max_length=200)


class Hours(CreatedUpdatedModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=200, choices=DAYS_OF_WEEK)
    open_range = IntegerRangeField()
    datetime_range = DateTimeRangeField()

    class Meta:
        ordering = ['-datetime_range']
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping',
                expressions=[
                    ('day_of_week', RangeOperators.EQUAL),
                    ('open_range', RangeOperators.OVERLAPS),
                    ('datetime_range', RangeOperators.OVERLAPS),
                ],
            ),
        ]
