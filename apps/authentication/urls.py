from django.conf import settings
from django.conf.urls import url
from django.urls import include

from apps.authentication import views

urlpatterns = []

if getattr(settings, "AUTH_ADD_URLS", False):
    urlpatterns += [
        url(r"^auth/email/login/$", views.EmailLoginView.as_view(), name="email-login"),
        url(
            r"^auth/email/signup/$",
            views.EmailSignupView.as_view(),
            name="email-signup",
        ),
        url(
            r"^auth/email/verify/$",
            views.VerifyEmailView.as_view(),
            name="email-verify",
        ),
        url(
            r"^auth/token/refresh/$",
            views.RefreshJWTView.as_view(),
            name="refresh-token",
        ),
    ]
