from django.contrib import admin
from .models import PurchaseOrder,OrderedProduct

# Register your models here.

admin.site.register(PurchaseOrder)
admin.site.register(OrderedProduct)