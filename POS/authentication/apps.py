from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    def ready(self):
        try:
            from django.contrib.auth.models import Group
            from django.db import models

            # Remove unique constraint on the name field
            Group._meta.get_field('name').blank = True
            Group._meta.get_field('name').null = True
            
           

        except ImportError:
            pass