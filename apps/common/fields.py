from django.urls import NoReverseMatch
from rest_framework.relations import HyperlinkedRelatedField


class URLArgsHyperlinkedRelatedField(HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        try:
            return super().get_url(obj, view_name, request, format)
        except NoReverseMatch:
            lookup_value = getattr(obj, self.lookup_field)
            kwargs = {self.lookup_url_kwarg: lookup_value}

            url_kwargs = request._request.resolver_match.kwargs

            kwargs.update(url_kwargs)

            return self.reverse(
                view_name, kwargs=kwargs, request=request, format=format
            )
