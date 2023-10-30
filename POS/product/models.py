from django.db import models
from main.models import Pharmacy
from suppliers.models import Supplier

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(null=True, unique=True, max_length=50)
    shorthand = models.CharField(null=True, unique=True, max_length=50)


class Product(models.Model):
    code = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    item_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2)

    minimum_stock_level = models.IntegerField()

    expiry_date = models.DateField(null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
