from django_filters import rest_framework as filters


class RestaurantFilter(filters.FilterSet):
    time = filters.IsoDateTimeFilter(required=True)

    @property
    def qs(self):
        return self.queryset.get_open_restaurants(self.data['time'])
