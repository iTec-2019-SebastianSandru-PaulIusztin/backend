from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.shop import views

seller_router = routers.DefaultRouter()
seller_router.register(r"sellers", views.SellerViewSet)
store_router = routers.DefaultRouter()
store_router.register(r"stores", views.StoreViewSet)
product_router = routers.DefaultRouter()
product_router.register(r"products", views.ProductViewSet)
category_router = routers.DefaultRouter()
category_router.register(r"products/categories", views.ProductCategoryViewSet)
subcategory_router = routers.DefaultRouter()
subcategory_router.register(r"products/subcategories", views.ProductSubcategoryViewSet)
payments_router = routers.DefaultRouter()
payments_router.register(r"payments", views.PaymentViewSet)

urlpatterns = [
    url(r"^buyer/me/$", views.CurrentBuyerView.as_view(), name="buyer-me"),
    url(
        r"^buyer/seller/$", views.CurrentSellerView.as_view(), name="seller-me"
    ),
    url(
        r"^buyer/shop-cart/$", views.CurrentShopCartView.as_view(), name="shop-cart-me"
    ),
    url(
        r"^stores/me/$", views.CurrentStoreView.as_view(), name="stores-me"
    ),
    url(
        r"^sellers/(?P<pk>\d+)/$", views.SellerStoreView.as_view(), name="seller-store"
    ),

    url(r"^", include(store_router.urls)),
    url(r"^", include(product_router.urls)),
    url(r"^", include(category_router.urls)),
    url(r"^", include(subcategory_router.urls)),
    url(r"^", include(payments_router.urls)),
]
