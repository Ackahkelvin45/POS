from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(verbose_name='email',unique=True,null=True,max_length=60,blank=True)
    username=models.CharField(max_length=50,null=True,blank=True)
    first_name=models.CharField(max_length=60,null=True,blank=True)
    last_name=models.CharField(max_length=60,null=True,blank=True)
    other_names=models.CharField(max_length=60,null=True,blank=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    date_joined=models.DateTimeField(null=True, blank=True,auto_now_add=True,verbose_name='date joined')
    last_login=models.DateTimeField(null=True,auto_now=True,)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    pharmacys=models.ManyToManyField("main.Pharmacy",related_name="admin",blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
Group.add_to_class('pharmacy', models.CharField(max_length=100, null=True, blank=True))


Group.add_to_class('custom_name', models.CharField(max_length=100, null=True, blank=True))



def _alternative_group_representation(self) -> str:

    return str(self.custom_name) 

Group.add_to_class('__str__', _alternative_group_representation)
      
    