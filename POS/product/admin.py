from django.contrib import admin
from .models import Subcategory, Category, Unit, Product

# Register your models here.

admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
