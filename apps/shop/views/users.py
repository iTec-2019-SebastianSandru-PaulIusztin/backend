from django.http import Http404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.authentication.views import CurrentUserView as DefaultCurrentUserView
from apps.common.backends import SearchFilterBackend
from apps.common.mixins import ServiceMixin
from apps.common.views import CreateRetrieveUpdateDestroyAPIView
from apps.shop import models
from apps.shop import serializers
from apps.shop import services


class CurrentBuyerView(ServiceMixin, DefaultCurrentUserView):
    queryset = models.Buyer.objects.all()
    serializer_class = serializers.BuyerSerializer
    service_class = services.UserService

    def get_object(self):
        user = super().get_object()

        self.get_service().on_retrieve(user)

        return user


class CurrentSellerView(CreateRetrieveUpdateDestroyAPIView):
    queryset = models.Seller.objects.all()
    serializer_class = serializers.SellerSerializer

    def get_object(self):
        try:
            seller = self.request.user.seller
        except models.Buyer.seller.RelatedObjectDoesNotExist:
            raise Http404()

        return seller


class SellerViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = models.Seller.objects.all()
    serializer_class = serializers.SellerSerializer
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)
