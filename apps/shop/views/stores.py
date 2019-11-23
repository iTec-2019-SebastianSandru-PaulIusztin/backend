from django.http import Http404
from rest_framework.viewsets import ModelViewSet

from apps.common.backends import SearchFilterBackend
from apps.common.views import CreateRetrieveUpdateDestroyAPIView
from apps.shop import models
from apps.shop import serializers


class StoreViewSet(ModelViewSet):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)


class CurrentStoreView(CreateRetrieveUpdateDestroyAPIView):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer

    def get_object(self):
        try:
            seller = self.request.user.seller
        except models.Buyer.seller.RelatedObjectDoesNotExist:
            raise Http404()

        try:
            store = seller.store
        except models.Buyer.seller.store.RelatedObjectDoesNotExist:
            raise Http404()

        return store
