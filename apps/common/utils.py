from typing import Type

from django.db.models import Model
from rest_framework.serializers import ModelSerializer


def get_or_create_model(
    validated_data: dict, serializer_class: Type[ModelSerializer], **kwargs
) -> Model:
    serializer = serializer_class(data=validated_data)
    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data
    validated_data.update(**kwargs)

    model_type = serializer.Meta.model
    instance, _ = model_type.objects.get_or_create(**validated_data)

    return instance
