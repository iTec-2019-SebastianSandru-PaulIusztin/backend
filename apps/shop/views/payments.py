from rest_framework.viewsets import ModelViewSet

from apps.shop import serializers
from apps.shop import models


class PaymentViewSet(ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(buyer__id=user.id)
