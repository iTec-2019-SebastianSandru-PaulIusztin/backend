import re

from django.apps import apps
from rest_framework import serializers
from rest_framework.fields import empty

from apps.common.fields import URLArgsHyperlinkedRelatedField


class NamespaceHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Simply adds the namespace to the view name for url related fields.
    The name of the app where the model is coming from is considered the namespace.
    """

    NAMESPACES = {
        model.__name__: app.label
        for app in apps.get_app_configs()
        for model in app.get_models()
    }
    LINK_CLASSES = (
        serializers.HyperlinkedRelatedField,
        serializers.HyperlinkedIdentityField,
        URLArgsHyperlinkedRelatedField,
    )

    def build_url_field(self, field_name, model_class):
        field_class, field_kwargs = super().build_url_field(field_name, model_class)
        if field_class in self.LINK_CLASSES:
            namespace = self.NAMESPACES[model_class.__name__]
            field_kwargs["view_name"] = "{namespace}:{name}".format(
                namespace=namespace, name=field_kwargs["view_name"]
            )

        return field_class, field_kwargs

    def build_relational_field(self, field_name, relation_info):
        field_class, field_kwargs = super().build_relational_field(
            field_name, relation_info
        )
        if field_class in self.LINK_CLASSES:
            namespace = self.NAMESPACES[relation_info.related_model.__name__]
            field_kwargs["view_name"] = "{namespace}:{name}".format(
                namespace=namespace, name=field_kwargs["view_name"]
            )

        return field_class, field_kwargs


class AutoIdAndUrlModelSerializer(NamespaceHyperlinkedModelSerializer):
    """
    Adds the option to represent a related object via id or url,
    without setting it explicitly in the serializer.
    The field names needs to be added to Meta.auto_related_fields
    """

    # TODO: Is this class a good idea ? Isn't it too much magic ?
    PATTERN = re.compile(r"(?P<field>.*)_(?P<suffix>urls?|ids?)$")

    def __init__(self, instance=None, data=empty, **kwargs):
        if hasattr(self.Meta, "auto_related_fields"):
            self.Meta.fields = self.Meta.fields + self.Meta.auto_related_fields

        super().__init__(instance, data, **kwargs)

    def build_field(self, field_name, info, model_class, nested_depth):
        match = self.PATTERN.match(field_name)
        if match:
            base_field = match.groupdict().get("field")
            suffix = match.groupdict().get("suffix")

            if base_field not in info.relations:
                return super().build_field(field_name, info, model_class, nested_depth)

            mapping = {
                "id": serializers.PrimaryKeyRelatedField,
                "ids": serializers.PrimaryKeyRelatedField,
                "url": URLArgsHyperlinkedRelatedField,
                "urls": URLArgsHyperlinkedRelatedField,
            }

            related_class = mapping[suffix]
            self.serializer_related_field = related_class

            field_class, field_kwargs = super().build_field(
                base_field, info, model_class, nested_depth
            )
            field_kwargs.update({"source": base_field})

            return field_class, field_kwargs
        else:
            self.serializer_related_field = serializers.HyperlinkedRelatedField

        return super().build_field(field_name, info, model_class, nested_depth)
