from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework import serializers

from apps.shop.models import Store
from apps.shop.serializers.products import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=40)
    lng = serializers.DecimalField(max_digits=50, decimal_places=40)

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ("name", "lat", "lng", "products")

    def create(self, validated_data):
        user = self.context['request'].user
        seller_id = user.seller.id

        lat = validated_data.pop('lat')
        lng = validated_data.pop('lng')

        point = Point(float(lng), float(lat))
        validated_data.update({"seller_id": seller_id, "point": point})

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
