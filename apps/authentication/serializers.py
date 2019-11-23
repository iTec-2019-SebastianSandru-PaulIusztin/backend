from allauth.account.models import EmailAddress
from django.conf import settings
from rest_auth.registration.serializers import (
    RegisterSerializer as RestRegisterSerializer,
)
from rest_auth.serializers import LoginSerializer as RestLoginSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer

from apps.authentication.utils import get_auth_model_class
from apps.authentication.utils import get_class_from_path


class UserSerializer(ModelSerializer):
    is_first_login = serializers.ReadOnlyField()

    class Meta:
        model = get_auth_model_class()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "photo",
            "is_staff",
            "is_first_login",
        )
        read_only_fields = ("id", "email", "username", "is_staff", "is_first_login")


class EmailLoginSerializer(RestLoginSerializer):
    username = None

    def validate_email(self, value):
        try:
            EmailAddress.objects.get(email=value)
        except EmailAddress.DoesNotExist:
            return value

        return str(value)


class EmailSignupSerializer(RestRegisterSerializer):
    username = None

    def get_cleaned_data(self):
        return self.validated_data


class VerifyEmailSerializer(serializers.Serializer):
    code = serializers.CharField(source="key")


class RefreshJWTSerializer(RefreshJSONWebTokenSerializer):
    def _check_user(self, payload):
        backend = self._get_jwt_auth_backend_class()

        assert backend is not None

        backend = backend()

        return backend.authenticate_credentials(payload)

    def _get_jwt_auth_backend_class(self):
        backends = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]

        for backend_path in backends:
            backend_class = get_class_from_path(backend_path)
            if issubclass(backend_class, JSONWebTokenAuthentication):
                return backend_class

        return None
