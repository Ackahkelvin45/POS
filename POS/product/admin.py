from django.contrib import admin
from .models import Subcategory, Category, Unit, Product_Item,Package

# Register your models here.
admin.site.register(Product_Item)
admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Package)

