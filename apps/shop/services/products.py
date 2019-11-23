from django.db.models import QuerySet

from apps.common.services import BaseService
from apps.shop import models


class ProductCategoryService(BaseService):
    def on_list(self, queryset: QuerySet):
        return models.ProductCategoryManager.order_by_counter(queryset)


class ProductSubcategoryService(BaseService):
    def on_list(self, queryset: QuerySet):
        return models.ProductSubcategoryManager.order_by_counter(queryset)


class ProductService(BaseService):
    def on_create(self, instance: models.Product):
        instance.increment_category()
        instance.increment_subcategories()

    def on_update(self, instance: models.Product, new_validated_data: dict):
        new_product_category = new_validated_data.get("category")
        if new_product_category:
            instance.increment_category()

        new_product_subcategories = new_validated_data.get("subcategories")
        if new_product_subcategories:
            new_product_subcategory_names = [
                product_subcategory["name"] for product_subcategory in new_product_subcategories
            ]
            instance.increment_subcategories(new_product_subcategory_names)
