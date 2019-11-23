import django_filters
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django_filters.constants import EMPTY_VALUES


class LatLngFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        lat, lng = value.split("#")
        point = Point(float(lng), float(lat))

        return qs.filter(store__point__distance_lt=(point, Distance(km=100)))


class ProductFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )
    latlng = LatLngFilter()
