from typing import List

from django.db import transaction
from django.db.models import Model
from rest_framework import serializers

from apps.common.utils import get_or_create_model
from apps.shop.models import ProductSubcategory, ProductPhoto, Product, Store, ShopCart, ShopCartItem
from apps.shop.models import ProductCategory
from apps.shop.serializers.users import SellerSerializer


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
        model = ProductPhoto
        fields = (
            "photo",
        )


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    category = ProductCategorySerializer()
    subcategories = ProductSubcategorySerializer(many=True)
    photos = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "counter",
            "product_type",
            "price",
            "description",
            "origin_type",
            "store_id",
            "category",
            "subcategories",
            "photos",
            "store_name",
            "seller",
            "lat",
            "lng"
        )
        read_only_fields = ("id", )

    def create(self, validated_data):
        category = validated_data.pop('category')
        subcategories = validated_data.pop('subcategories')
        photos = validated_data.pop('photos')

        store = self.context['request'].user.seller.store

        with transaction.atomic():
            category = self._get_or_create_category(category)

            validated_data.update({"category": category, "store": store})

            product = Product(**validated_data)
            product.save()

            self._get_or_create_subcategories(product, subcategories)
            self._get_or_create_photos(product, photos)

        return product

    def update(self, instance, validated_data):
        category = validated_data.pop("category", None)
        subcategories = validated_data.pop("subcategories", None)
        photos = validated_data.pop('photos')

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

            if photos is not None:
                self._get_or_create_photos(instance, photos)

        return instance

    def _get_or_create_category(self, category: dict) -> Model:
        return get_or_create_model(category, ProductCategorySerializer)

    def _get_or_create_subcategories(self, product: Product, subcategories: List[dict]):
        for subcategory in subcategories:
            subcategory = get_or_create_model(subcategory, ProductSubcategorySerializer)
            product.subcategories.add(subcategory)

    def _get_or_create_photos(self, product: Product, photos: List[dict]):
        for photo in photos:
            get_or_create_model(photo, PhotoSerializer, product=product)


class ShopCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )

    class Meta:
        model = ShopCartItem
        fields = ('product', 'product_id')


class ShopCartSerializer(serializers.ModelSerializer):
    items = ShopCartItemSerializer(many=True)

    class Meta:
        model = ShopCart
        fields = ('items', )

    def create(self, validated_data):
        items = validated_data.pop('items')
        user = self.context['request'].user

        validated_data.update({'buyer': user})

        with transaction.atomic():
            shop_cart = ShopCart(**validated_data)
            shop_cart.save()

            self._get_or_create_items(shop_cart, items)

        return shop_cart

    def update(self, instance, validated_data):
        items = validated_data.pop('items')

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            if items is not None:
                self._get_or_create_items(instance, items)

        return instance

    def _get_or_create_items(self, shop_cart: ShopCart, items: List[dict]):
        for item in items:
            item['product_id'] = item['product'].id
            get_or_create_model(item, ShopCartItemSerializer, shop_cart=shop_cart)
