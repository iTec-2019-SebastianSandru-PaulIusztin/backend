from django.db.models import Model
from django.db.models import QuerySet

from apps.common.choices import DRFActions
from apps.common.choices import RESTMethods


class BaseService:
    """
        Base service layer for domain logic between network and database layers.
    """

    _get_service_key = object()

    def __init__(self, get_service_key, request):
        """
        :param get_service_key: Parameter that is making the constructor private.
        """
        assert (
            get_service_key == self._get_service_key
        ), "Service must be created only with the staticmethod 'get_service(view)'"

        self._request = request

    @classmethod
    def get_service(cls, view):
        service_class = getattr(view, "service_class", None)

        assert service_class is not None

        return service_class(cls._get_service_key, view.request)

    @staticmethod
    def should_perform(view, choice_actions, choice_method):
        action = getattr(view, "action", None)
        method = getattr(view.request, "method", None)

        if isinstance(choice_actions, str):
            choice_actions = [choice_actions]

        return (action and action in choice_actions) or (
            not action and method == choice_method
        )

    def on_create(self, instance: Model):
        """
        :param instance: The newly created model.
        """
        pass

    def on_list(self, queryset: QuerySet):
        return queryset

    def on_retrieve(self, instance: Model):
        return instance

    def on_update(self, instance: Model, new_validated_data: dict):
        """
        :param instance: The updated model.
        :param new_validated_data: The new data that was patched to the instance.
        """
        pass

    def on_destroy(self, instance: Model):
        """
        :param instance: The model before it's deleted.
        """
        pass
