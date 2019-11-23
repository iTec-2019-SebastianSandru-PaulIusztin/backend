# FIXME: Make a system that is announcing the user that it has to call the super methods when it is overriding them.
from apps.common.choices import DRFActions
from apps.common.choices import RESTMethods
from apps.common.services import BaseService


class CreateServiceMixin:
    service_class = None

    def perform_create(self, serializer):
        assert self.service_class is not None

        super().perform_create(serializer)

        if self.should_perform_on_create():
            instance = serializer.instance
            service_instance = BaseService.get_service(self)
            service_instance.on_create(instance)

    def should_perform_on_create(self):
        return BaseService.should_perform(self, DRFActions.CREATE, RESTMethods.POST)


class ListServiceMixin:
    service_class = None

    def get_queryset(self):
        assert self.service_class is not None

        queryset = super().get_queryset()

        if self.should_perform_on_list():
            service_instance = BaseService.get_service(self)
            queryset = service_instance.on_list(queryset)

        assert queryset is not None

        return queryset

    def should_perform_on_list(self):
        return BaseService.should_perform(self, DRFActions.LIST, RESTMethods.GET)


class RetrieveServiceMixin:
    service_class = None

    def get_object(self):
        assert self.service_class is not None

        instance = super().get_object()

        if self.should_perform_on_retrieve():
            service_instance = BaseService.get_service(self)
            instance = service_instance.on_retrieve(instance)

        assert instance is not None

        return instance

    def should_perform_on_retrieve(self):
        return BaseService.should_perform(self, DRFActions.RETRIEVE, RESTMethods.GET)


class UpdateServiceMixin:
    service_class = None

    def perform_update(self, serializer):
        assert self.service_class is not None

        super().perform_update(serializer)

        if self.should_perform_on_update():
            instance = serializer.instance
            new_validated_data = serializer.validated_data

            service_instance = BaseService.get_service(self)
            service_instance.on_update(instance, new_validated_data)

    def should_perform_on_update(self):
        return BaseService.should_perform(self, [DRFActions.UPDATE, DRFActions.PARTIAL_UPDATE], RESTMethods.PATCH)


class DestroyServiceMixin:
    service_class = None

    def perform_destroy(self, instance):
        assert self.service_class is not None

        if self.should_perform_on_destroy():
            service_instance = BaseService.get_service(self)
            service_instance.on_destroy(instance)

        super().perform_destroy(instance)

    def should_perform_on_destroy(self):
        return BaseService.should_perform(self, DRFActions.DESTROY, RESTMethods.DELETE)


class ServiceMixin(
    CreateServiceMixin,
    ListServiceMixin,
    RetrieveServiceMixin,
    UpdateServiceMixin,
    DestroyServiceMixin,
):
    def get_service(self):
        return self.service_class.get_service(self)
