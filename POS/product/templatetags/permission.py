# permissions_filters.py
from django import template
from django.contrib.auth.models import Permission
from django_tenants.utils import schema_context

register = template.Library()

@register.filter(name='has_global_permission')
def has_global_permission(user,app_label):
    # Save the current schema
   

    # Set the schema to the public schema
    with schema_context("public"):

        # Check if the user's group has the specified permission
        user_group= user.groups.first()
        has_permission = (
            user_group.permissions.filter(content_type__app_label=app_label).exists()
            if user_group
            else False
        )

        return has_permission