from typing import List

from django.db import transaction
from django.db.models import Model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.authentication.serializers import UserSerializer as DefaultUserSerializer
from apps.common.utils import get_or_create_model
from apps.shop import models, choices


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ("country", "county", "city", "street" )


class SellerSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = models.Seller
        fields = (
            "id",
            "address",
            "name",
            "phone",
            "buyer_type",
            "photo"
        )

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        address = validated_data.pop("address")

        with transaction.atomic():
            address = self._create_address(address)
            validated_data.update({"buyer": user, "address": address})

            seller = models.Seller(**validated_data)
            seller.save()

        return seller

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if address is not None:
                address = self._create_address(address)
                instance.address = address

            instance.save()

        return instance

    def _create_address(self, address: dict) -> Model:
        return get_or_create_model(address, AddressSerializer)


class BuyerSerializer(DefaultUserSerializer):
    seller = SellerSerializer(read_only=True)
    address = AddressSerializer()

    phone = PhoneNumberField()
    buyer_type = serializers.ChoiceField(choices=choices.BuyerTypeChoices.BUYER_TYPE_CHOICES)
    is_seller = serializers.BooleanField()

    class Meta(DefaultUserSerializer.Meta):
        fields = DefaultUserSerializer.Meta.fields + ("seller", "address", "phone", "buyer_type", "is_seller")

    def create(self, validated_data):
        address = validated_data.pop("address")

        with transaction.atomic():
            address = self._create_address(address)
            validated_data.update({"address": address})

            buyer = models.Buyer(**validated_data)
            buyer.save()

        return buyer

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            if address is not None:
                address = self._create_address(address)
                instance.address = address

            instance.save()

        return instance

    def _create_address(self, address: dict) -> Model:
        return get_or_create_model(address, AddressSerializer)
