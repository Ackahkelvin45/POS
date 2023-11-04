# custom_filters.py

from django import template

register = template.Library()

@register.filter
def chunk_string(value, chunk_size=15):
    return [value[i:i+chunk_size] for i in range(0, len(value), chunk_size)]
