from django.db import models

# Create your models here.

class Supplier(models.Model):
    company_name = models.CharField(max_length=300, unique=True, null=True)
    first_name = models.CharField(max_length=100, null=True)
    other_names=models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True,unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)
    phone_number_1 = models.CharField(max_length=100, null=True, unique=True)
    phone_number_2 = models.CharField(max_length=100, null=True, unique=True)
    website = models.URLField(max_length=200, null=True, unique=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='date created')
    is_active = models.BooleanField(default=True, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True, blank=True)
    opening_balance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True ,default=0)

    
    