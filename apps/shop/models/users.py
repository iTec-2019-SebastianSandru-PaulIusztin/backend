from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.authentication.models import AbstractUser
from apps.authentication.models import UserManager as DefaultUserManager
from apps.authentication.utils import get_photos_path_creator
from apps.shop import choices
from main import settings


class Address(models.Model):
    country = models.CharField(max_length=64)
    county = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=256)


class BuyerManager(DefaultUserManager):
    pass


class Buyer(AbstractUser):

    objects = BuyerManager()

    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='buyer', null=True)

    phone = PhoneNumberField()
    buyer_type = models.CharField(max_length=16, choices=choices.BuyerTypeChoices.BUYER_TYPE_CHOICES)

    class Meta:
        db_table = "authentication_user"


class Seller(models.Model):
    buyer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='seller', null=True)

    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    buyer_type = models.CharField(max_length=16, choices=choices.BuyerTypeChoices.BUYER_TYPE_CHOICES)
    photo = models.ImageField(
        upload_to=get_photos_path_creator(field_name="photo"), blank=True, null=True
    )
