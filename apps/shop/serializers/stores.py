from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework import serializers

from apps.shop.models import Store, Seller
from apps.shop.serializers import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=40)
    lng = serializers.DecimalField(max_digits=50, decimal_places=40)

    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller')
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ("name", "lat", "lng", "seller_id", "products")

    def create(self, validated_data):
        lat = validated_data.pop('lat')
        lng = validated_data.pop('lng')

        point = Point(float(lng), float(lat))
        validated_data.update({"point": point})

        store = Store(**validated_data)
        store.save()

        return store

    def update(self, instance, validated_data):
        lat = validated_data.pop('lat')
        lng = validated_data.pop('lng')

        if (lat and not lng) or (lng and not lat):
            raise serializers.ValidationError()

        if lat and lng:
            point = Point(float(lng), float(lat))
            validated_data.update({"point": point})

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance
