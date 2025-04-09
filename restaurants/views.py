from rest_framework.generics import ListAPIView

from restaurants.filters import RestaurantFilter
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class RestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_class = RestaurantFilter
