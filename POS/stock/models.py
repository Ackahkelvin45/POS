from django.db import models
from product.models import Product_Item
from purchases.models import PurchaseOrder

# Create your models here.
class ReceivedStock(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product_Item, on_delete=models.CASCADE, null=True)
    received_quantity = models.PositiveIntegerField(default=0,null=True)
    received_at = models.DateField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        super(ReceivedStock, self).save(*args, **kwargs)

        # Update the available quantity in the Product_Item model
        product = self.product
        product.available_quantity += self.received_quantity
        product.save()

        # Check if all products in the purchase order are received
        ordered_products = self.purchase_order.orderedproduct_set.all()        
        received_quantity_sum = ReceivedStock.objects.filter(
            purchase_order=self.purchase_order,
            product__in=ordered_products.values_list('product', flat=True)
        ).aggregate(Sum('received_quantity'))['received_quantity__sum']

        if received_quantity_sum is not None and received_quantity_sum == self.purchase_order.total_quantity:
            # All products in the purchase order are received
            self.purchase_order.status = 'received'
        elif received_quantity_sum is not None and received_quantity_sum > 0:
            # Some products are received, but not all
            self.purchase_order.status = 'partially received'
        else:
            # No products are received
            self.purchase_order.status = 'pending'

        self.purchase_order.save()

