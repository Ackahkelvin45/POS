from django.db import models
from product.models import Product_Item,Package
from authentication.models import User
from . import utils
from django.utils import timezone
# Create your models here.


class Tax(models.Model):
    name = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True)


class PaymentDetails(models.Model):
    payment_type = models.CharField(null=True, max_length=100)
    amount_paid = models.DecimalField(max_digits=5, decimal_places=2, null=True,default=0)
    change = models.DecimalField(max_digits=5, decimal_places=2, null=True,default=0)
    balance= models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True,default=0)
    
    
class Sale(models.Model):
    products = models.ManyToManyField(Product_Item, through='SaleProduct')
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    total_quantity = models.PositiveIntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True,default=0)
    tax = models.ManyToManyField(Tax,related_name="sale_tax")
    invoice_number = models.CharField(null=True, blank=True)
    sale_number = models.CharField(max_length=12,null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_created = models.DateTimeField( null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=20, null=True)
    sub_total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    payment = models.ForeignKey(PaymentDetails, null=True, on_delete=models.CASCADE, related_name='sales_item')
    
 
    def save(self, *args, **kwargs):
        if not self.sale_number:
            # If the osale number is not set, generate a unique number
            self.sale_number = utils.generate_unique_sale_number()

        # Calculate totals
        if self.pk:
            saleproducts = self.saleproduct_set.all()
            total_cost_price = sum(op.total_cost_price for op in saleproducts)
            self.sub_total_cost_price =sum(op.total_cost_price for op in saleproducts)
            total_quantity = sum(op.quantity for op in saleproducts)

            if self.discount:
                original_price = total_cost_price
                discount_price = (self.discount / 100) * original_price
                new_price = original_price - discount_price
                total_cost_price = new_price
                print("discount")

            if self.tax:
                for tax in self.tax.all():
                    total_cost_price += tax.amount 

            # Set calculated totals
            self.total_cost_price = total_cost_price
            self.total_quantity = total_quantity


        # Call the original save method to save the instance
        super(Sale, self).save(*args, **kwargs)

class  SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING,null=True)
    product = models.ForeignKey(Product_Item, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    cost_unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    package_type = models.ForeignKey(Package, on_delete=models.DO_NOTHING, null=True,blank=True)
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)




  

    def calculate_total_cost_price(self):
        self.total_cost_price = (self.quantity) * self.cost_unit_price
        



class PausedSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False, null=True)
    