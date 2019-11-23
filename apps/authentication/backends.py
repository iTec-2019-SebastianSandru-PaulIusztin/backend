from django.utils.translation import gettext
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.authentication.utils import get_auth_model_class


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        User = get_auth_model_class()
        user_id = payload.get("user_id")

        if user_id is None:
            raise exceptions.AuthenticationFailed(gettext("Invalid payload."))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(gettext("Invalid signature."))

        if not user.is_active:
            raise exceptions.AuthenticationFailed(gettext("User account is disabled."))

        return user
