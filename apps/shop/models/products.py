from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F

from apps.authentication.utils import get_photos_path_creator
from apps.shop import choices
from apps.shop.models.stores import Store


################
# BaseCategory #
################


class BaseCategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    counter = models.BigIntegerField(default=0, validators=(MinValueValidator(0),))

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def increment_counter(self):
        self.counter += 1
        self.save()


class BaseCategoryManager(models.Manager):
    @staticmethod
    def order_by_counter(queryset):
        return queryset.order_by("-counter")


###############
# ProductCategory #
###############


class ProductCategoryManager(BaseCategoryManager):
    pass


class ProductCategory(BaseCategoryModel):
    objects = ProductCategoryManager()


##################
# ProductSubcategory #
##################


class ProductSubcategoryManager(BaseCategoryManager):
    pass


class ProductSubcategory(BaseCategoryModel):
    objects = ProductSubcategoryManager()


###########
# Product #
###########


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_query_name="products"
    )
    subcategories = models.ManyToManyField(
        ProductSubcategory, related_query_name="products"
    )

    counter = models.BigIntegerField(default=0, validators=(MinValueValidator(0),))
    product_type = models.CharField(max_length=16, choices=choices.ProductTypeChoices.PRODUCT_TYPE_CHOICES)
    origin_type = models.CharField(max_length=16, choices=choices.ProductOriginChoices.PRODUCT_ORIGIN_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=512)

    def increment_subcategories(self, subcategories_names=None):
        subcategories = self.subcategories
        if subcategories_names:
            subcategories = self.subcategories.filter(name__in=subcategories_names)

        return subcategories.update(counter=F("counter") + 1)

    def increment_category(self):
        return self.category.increment_counter()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to=get_photos_path_creator(field_name="photo"), blank=True, null=True)
