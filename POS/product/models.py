from django.db import models
from main.models import Pharmacy

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)
    

class Subcategory(models.Model):
    name = models.CharField(max_length=100, null=True,unique=True)
    code = models.CharField(max_length=100, null=True, unique=True)


    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(null=True, unique=True, max_length=50)
    shorthand=models.CharField(null=True,unique=True,max_length=50)