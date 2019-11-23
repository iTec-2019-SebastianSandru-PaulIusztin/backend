from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    try:
        return getattr(settings, name, "")
    except AttributeError:
        return ""
