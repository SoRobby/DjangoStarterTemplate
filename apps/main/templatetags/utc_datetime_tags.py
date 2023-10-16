from django import template
from django.utils.timezone import is_aware, make_naive, utc

register = template.Library()

@register.filter
def utc_standard(value):
    if is_aware(value):
        value = make_naive(value, timezone=utc)
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')

