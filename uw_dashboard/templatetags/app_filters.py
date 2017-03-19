from django import template

register = template.Library()

@register.filter
def get(mapping, key):
    value = mapping.get(key, '')
    return value