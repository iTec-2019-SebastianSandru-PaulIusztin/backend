from rest_framework.viewsets import ModelViewSet

from apps.shop import serializers
from apps.shop import models


class PaymentViewSet(ModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
