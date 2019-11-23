from django.shortcuts import render_to_response
from rest_auth import views as rest_auth_views
from rest_auth.registration import views as rest_auth_registration_views
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_jwt.views import RefreshJSONWebToken

from apps.authentication import serializers


class CurrentUserView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class EmailLoginView(rest_auth_views.LoginView):
    authentication_classes = ()
    serializer_class = serializers.EmailLoginSerializer


class EmailSignupView(rest_auth_registration_views.RegisterView):
    serializer_class = serializers.EmailSignupSerializer
    authentication_classes = ()


class VerifyEmailView(rest_auth_registration_views.VerifyEmailView):
    authentication_classes = ()

    def get_serializer(self, *args, **kwargs):
        return serializers.VerifyEmailSerializer(*args, **kwargs)


class RefreshJWTView(RefreshJSONWebToken):
    serializer_class = serializers.RefreshJWTSerializer
