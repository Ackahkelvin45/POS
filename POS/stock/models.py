from django.db import models
from product.models import Product_Item, Package
from django.db.models import Sum
from authentication.models  import User




class StockEntry(models.Model):
    product = models.ForeignKey(Product_Item, on_delete=models.CASCADE,null=True,blank=True)
    quantity_received = models.PositiveIntegerField(default=0,null=True,blank=True)
    previous_quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    available_quantity = models.PositiveIntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(null=True,blank=True)
    info = models.CharField(null=True, blank=True, max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    reason = models.CharField(null=True, blank=True, max_length=500)
    package_type=models.ForeignKey(Package, null=True, on_delete=models.DO_NOTHING, blank=True)

    def add_to_stock(self):
        if self.package_type:
            product = self.package_type
            product.available_quantity = product.available_quantity + self.quantity_received
            product.save()
            self.info = f"{self.package_type} updated by {self.quantity_received} manually"
        else:
            
            product = self.product
            product.available_quantity = product.available_quantity + self.quantity_received
            product.save()
            self.info = f"{self.product.name} updated by {self.quantity_received} manually"
    
    def change_stock(self):
        if self.package_type:
            product = self.package_type
            product.available_quantity =self.quantity_received
            product.save()
            self.info = f"{self.package_type} changed  to  {self.quantity_received} manually"
        else:
            product = self.product
            product.available_quantity =self.quantity_received
            product.save()
            self.info = f"{self.product.name} changed  to  {self.quantity_received} manually"


        

    def __str__(self):
        return f"{self.product.name} - {self.quantity_received} units"








