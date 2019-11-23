from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.shop import services
from apps.common.backends import SearchFilterBackend
from apps.common.mixins import ServiceMixin
from apps.shop import models, filters
from apps.shop import serializers


class ProductCategoryViewSet(ServiceMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer
    service_class = services.ProductCategoryService
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)


class ProductSubcategoryViewSet(ServiceMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.ProductSubcategory.objects.all()
    serializer_class = serializers.ProductSubcategorySerializer
    service_class = services.ProductSubcategoryService
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)


class ProductViewSet(ServiceMixin, ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    service_class = services.ProductService
    filter_backends = (SearchFilterBackend, DjangoFilterBackend)
    filter_class = filters.ProductFilter
    search_fields = ("subcategories__name", "store__seller__name")
