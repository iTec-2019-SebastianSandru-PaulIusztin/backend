import datetime
import hashlib
import importlib
import os
from calendar import timegm
from functools import partial

from django.conf import settings
from rest_framework_jwt.settings import api_settings


def get_class_from_path(class_path: str):
    """
       Attempt to import a class from a string representation.
   """
    try:
        module_path, class_name = class_path.rsplit(".", 1)
    except ValueError:
        # In case when class_path = class_name.
        module_path = "."
        class_name = class_path

    try:
        module = importlib.import_module(module_path)
        my_class = getattr(module, class_name)
    except (ImportError, AttributeError):
        msg = 'Could not import class "{}" .'.format(class_path)
        raise ImportError(msg)

    return my_class


def get_auth_model_class():
    module_path, auth_model_class = settings.AUTH_USER_MODEL.rsplit(".", 1)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_module_name = base_dir.split("/")[-1]

    class_path = f"{base_module_name}.{module_path}.models.{auth_model_class}"

    return get_class_from_path(class_path)


def jwt_payload_handler(user):
    payload = {
        "user_id": user.pk,
        "date_joined": str(user.date_joined),
        "exp": datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
    }

    if api_settings.JWT_ALLOW_REFRESH:
        payload["orig_iat"] = timegm(datetime.datetime.utcnow().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload["aud"] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload["iss"] = api_settings.JWT_ISSUER

    return payload


def upload_to_callback(field_name, category, instance, filename):
    assert hasattr(instance, field_name)

    field = getattr(instance, field_name)

    unique_identifier = hashlib.sha256(field.read()).hexdigest()
    model_name = instance.__class__.__name__.lower()
    _, extension = os.path.splitext(filename)

    return "{}/{}/{}{}".format(category, model_name, unique_identifier, extension)


def get_photos_path_creator(field_name: str):
    return partial(upload_to_callback, field_name, "photos")
