from typing import List

from django.db import transaction
from django.db.models import Model
from rest_framework import serializers

from apps.common.utils import get_or_create_model
from apps.shop.models import ProductSubcategory, ProductImage, Product, Store
from apps.shop.models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name",)

        extra_kwargs = {
            "name": {
                "validators": []
            }
        }


class ProductSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = ("name",)

        extra_kwargs = {
            "name": {
                "validators": []
            }
        }


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "photo",
        )


class ProductSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all(), source='store')

    category = ProductCategorySerializer()
    subcategories = ProductSubcategorySerializer(many=True)
    photos = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "counter",
            "product_type",
            "price",
            "description",
            "origin_type",
            "store_id",
            "category",
            "subcategories",
            "photos"
        )
        read_only_fields = ("id", )

    def create(self, validated_data):
        category = validated_data.pop('category')
        subcategories = validated_data.pop('subcategories')

        with transaction.atomic():
            category = self._get_or_create_category(category)

            validated_data.update({"category": category})

            product = Product(**validated_data)
            product.save()

            self._get_or_create_subcategories(product, subcategories)

        return product

    def update(self, instance, validated_data):
        category = validated_data.pop("category", None)
        subcategories = validated_data.pop("subcategories", None)

        with transaction.atomic():
            if category is not None:
                category = self._get_or_create_category(category)

                validated_data.update({"category": category})

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            if subcategories is not None:
                instance.subcategories.clear()
                self._get_or_create_subcategories(instance, subcategories)

        return instance

    def _get_or_create_category(self, category: dict) -> Model:
        return get_or_create_model(category, ProductCategorySerializer)

    def _get_or_create_subcategories(self, product: Product, subcategories: List[dict]):
        for subcategory in subcategories:
            subcategory = get_or_create_model(subcategory, ProductSubcategorySerializer)
            product.subcategories.add(subcategory)
