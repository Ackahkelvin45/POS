from django.contrib import admin
from .models import Sale,SaleProduct,Tax

# Register your models here.
admin.site.register(Sale)
admin.site.register(SaleProduct)
admin.site.register(Tax)