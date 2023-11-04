
from django.db import models
from suppliers.models import Supplier


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)
    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(null=True, unique=True, max_length=50)
    shorthand = models.CharField(null=True, unique=True, max_length=50)
    def __str__(self):
        return self.name


class Product_Item(models.Model):
    code = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,null=True, blank=True)
    item_unit = models.ForeignKey(Unit, on_delete=models.CASCADE,null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    markup = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    minimum_stock_level = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True, upload_to='product_images/')
    barcode = models.ImageField(upload_to='student_barcode/', blank=True, null=True)


    def __str__(self):
        return self.name


class Stock_Level(models.Model):
    new_quantity_recieved = models.IntegerField(null=True, blank=True)
    available_quantity = models.IntegerField(null=True, blank=True)
    


class Package(models.Model):
    product = models.ForeignKey(Product_Item,null=True, blank=True, on_delete=models.CASCADE)
    number_of_products_item = models.IntegerField(null=True, blank=True)
    unit=models.ForeignKey(Unit, on_delete=models.CASCADE,null=True, blank=True)
    package_name = models.CharField(max_length=100, null=True, unique=True)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2,null=True, blank=True)
    
    
    