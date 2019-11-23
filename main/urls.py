from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from apps.common.views import get_swagger_view
from apps.common.views import HealthView

urlpatterns = [
    url(r"^$", RedirectView.as_view(pattern_name="docs")),
    url(r"^api/docs/$", get_swagger_view(title=settings.PROJECT_NAME), name="docs"),
    url(
        r"^api/",
        include(
            ("apps.authentication.urls", "authentication"), namespace="authentication"
        ),
    ),
    url(r"^api/", include(("apps.shop.urls", "shop"), namespace="shop")),
    url(r"^health/$", HealthView.as_view(), name="health"),
    path("admin/", admin.site.urls),
]
