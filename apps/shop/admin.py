from django.contrib import admin

from apps.shop import models


class AddressAdmin(admin.ModelAdmin):
    list_display = ("city", "county", "street")
    search_fields = ("city", "county", "street")


class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


class ProductPhotoAdmin(admin.StackedInline):
    model = models.ProductPhoto
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("category", "counter", "price")
    inlines = [ProductPhotoAdmin]


class ShipmentInline(admin.StackedInline):
    model = models.Shipment
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('status', )
    inlines = [ShipmentInline]


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('status', )
    search_fields = ('status', )


class ShopCartItemAdmin(admin.StackedInline):
    model = models.ShopCartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', )


admin.site.register(models.Seller, SellerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Shipment, ShipmentAdmin)
admin.site.register(models.ShopCart, CartAdmin)
