from django.db import connection
from django.db import OperationalError
from django.http import JsonResponse
from django.views import View
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer


class HealthView(View):
    def get(self, request):
        try:
            connection.ensure_connection()
        except OperationalError as err:
            return JsonResponse({"message": str(err)}, status=503)

        return JsonResponse({"message": "ok"})


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [CoreJSONRenderer, OpenAPIRenderer, SwaggerUIRenderer]

        def get(self, request):
            generator = SchemaGenerator(
                title=title, url=url, patterns=patterns, urlconf=urlconf
            )
            schema = generator.get_schema(request=request, public=True)

            if not schema:
                raise exceptions.ValidationError(
                    "The schema generator did not return a schema Document"
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()


class CreateRetrieveUpdateDestroyAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):
    """
    Concrete view for creating, retrieving, updating or deleting a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
