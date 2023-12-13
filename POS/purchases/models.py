from django.db import models
from suppliers.models import Supplier
from authentication.models import User
from product.models import Product_Item, Package
from .  import utils
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Sum
from stock.models import StockEntry
from django.utils import timezone


# Create your models here.

Status= (
    ('pending', 'PENDING'),
    ('partially recieved', 'PARTIALLY RECIEVED'),
    ('recieved', 'RECIEVED'),
)


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING,null=True)
    products = models.ManyToManyField(Product_Item, through='OrderedProduct')
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    total_quantity=models.PositiveIntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    invoice_number = models.CharField(null=True, blank=True)
    order_number = models.CharField(max_length=12,null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    recieved_at = models.DateField( null=True)
    status = models.CharField(max_length=20, default='pending',choices=Status,null=True) 


    def update_order_status(self):
        remaining_quantity_sum = self.orderedproduct_set.aggregate(
            total_remaining_quantity=Sum('remaining_quantity')
        )['total_remaining_quantity']

        if remaining_quantity_sum == 0:
            # All products received
            self.status = 'recieved'
        elif remaining_quantity_sum > 0:
            # Some products received
            self.status = 'partially received'
        else:
            # No products received
            self.status = 'pending'

        self.save()
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # If the order number is not set, generate a unique number
            self.order_number = utils.generate_unique_order_number()

        # Calculate totals
        if self.pk:
            ordered_products = self.orderedproduct_set.all()
            total_cost_price = sum(op.total_cost_price for op in ordered_products)
            total_quantity = sum(op.quantity for op in ordered_products)

            if self.discount:
                original_price = total_cost_price
                discount_price = (self.discount / 100) * original_price
                new_price = original_price - discount_price
                total_cost_price = new_price
                print("discount")

            # Set calculated totals
            self.total_cost_price = total_cost_price
            self.total_quantity = total_quantity

        # Call the original save method to save the instance
        super(PurchaseOrder, self).save(*args, **kwargs)

 

class  OrderedProduct(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING,null=True)
    product = models.ForeignKey(Product_Item, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    cost_unit_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    package_type = models.ForeignKey(Package, on_delete=models.DO_NOTHING, null=True,blank=True)
    total_cost_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    received_quantity = models.PositiveIntegerField(default=0, null=True)
    remaining_quantity = models.PositiveIntegerField(default=0, null=True)





        

    def save(self, *args, **kwargs):

        self.remaining_quantity = self.quantity-self.received_quantity

            


        super(OrderedProduct, self).save(*args, **kwargs)

    def calculate_quantity(self):
                    
        if self.package_type:
            # If there's a package type, use its number_of_products_item for multiplication
            multiplier = self.package_type.number_of_products_item
        else:
            # If there's no package type, assume a multiplier of 1
            multiplier = 1

        self.quantity = self.quantity * multiplier

    def calculate_total_cost_price(self):
        self.total_cost_price = (self.quantity) * self.cost_unit_price
        
    def add_to_stock(self,user,quantity):
        stockentry = StockEntry(
            product=self.product,
            quantity_received=quantity,
             previous_quantity=self.product.available_quantity,
            user=user,
            created_at=timezone.now(),
        )

        
        product = self.product
        product.available_quantity = self.received_quantity
        product.save()
        stockentry.available_quantity = product.available_quantity
        stockentry.info=f"{self.product.name } updated by {quantity} in purchase order {self.purchase_order.order_number}"
        stockentry.save()
        self.save()


      

class ReceivedProductHistory(models.Model):
    ordered_product = models.ForeignKey(OrderedProduct, on_delete=models.CASCADE)
    received_quantity = models.PositiveIntegerField(null=True)
    received_time = models.DateTimeField(auto_now_add=True)

    