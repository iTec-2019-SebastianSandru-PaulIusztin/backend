from rest_framework.viewsets import ModelViewSet

from apps.common.backends import SearchFilterBackend
from apps.shop import models
from apps.shop import serializers


class StoreViewSet(ModelViewSet):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
    filter_backends = (SearchFilterBackend,)
    search_fields = ("name",)
