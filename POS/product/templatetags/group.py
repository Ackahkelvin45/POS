from django_tenants.utils import schema_context
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag
def get_user_group(user):
    with schema_context("public"):

        return    user.groups.first()
   