from django import template

register = template.Library()


@register.filter(name='verbose_name')
def verbose_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()
