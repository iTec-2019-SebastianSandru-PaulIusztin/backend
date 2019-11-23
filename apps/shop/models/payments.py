from django.core.validators import MinValueValidator
from django.db import models

from apps.shop import choices
from apps.shop.models import Product


class Payment(models.Model):
    status = models.CharField(max_length=16, choices=choices.PaymentChoices.PAYMENT_CHOICES)
    optional = models.TextField(max_length=521, null=True, blank=True)


class PaymentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payment_products')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_products')

    counter = models.BigIntegerField(default=0, validators=(MinValueValidator(0),))


class Shipment(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='shipment')

    status = models.CharField(max_length=16, choices=choices.ShipmentChoices.SHIPPING_CHOICES)
    provider = models.CharField(max_length=16, choices=choices.ShippingProviderChoices.PROVIDER_CHOICES)
