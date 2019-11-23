from django.contrib import admin

from apps.shop import models


class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


class ProductPhotoAdmin(admin.StackedInline):
    model = models.ProductPhoto
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ("category", "counter", "price")
    inlines = [ProductPhotoAdmin]


admin.site.register(models.Seller, SellerAdmin)
admin.site.register(models.Product, ProductAdmin)
