from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.common.views import CreateRetrieveUpdateDestroyAPIView
from apps.shop import services
from apps.common.backends import SearchFilterBackend
from apps.common.mixins import ServiceMixin
from apps.shop import models, filters
from apps.shop import serializers


class ProductCategoryViewSet(ServiceMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer
    authentication_classes = ()
    permission_classes = ()
    service_class = services.ProductCategoryService
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)


class ProductSubcategoryViewSet(ServiceMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.ProductSubcategory.objects.all()
    serializer_class = serializers.ProductSubcategorySerializer
    authentication_classes = ()
    permission_classes = ()
    service_class = services.ProductSubcategoryService
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)


class ProductViewSet(ServiceMixin, ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    service_class = services.ProductService
    authentication_classes = ()
    permission_classes = ()
    filter_backends = (SearchFilterBackend, DjangoFilterBackend)
    filter_class = filters.ProductFilter
    search_fields = ("subcategories__name", "store__seller__name", "price")


class CurrentShopCartView(CreateRetrieveUpdateDestroyAPIView):
    queryset = models.ShopCart.objects.all()
    serializer_class = serializers.ShopCartSerializer

    def get_object(self):
        try:
            seller = self.request.user.shop_cart
        except models.Buyer.shop_cart.RelatedObjectDoesNotExist:
            raise Http404()

        return seller
