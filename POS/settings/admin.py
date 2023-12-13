from django.contrib import admin
from .models import EmailBackend,AppSettings

# Register your models here.

admin.site.register(EmailBackend)
admin.site.register(AppSettings)