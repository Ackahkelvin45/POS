from django.db import models
from django.contrib.auth.models import AbstractUser
#from main.models import Pharmacy
# Create your models here.
class User(AbstractUser):
    email=models.EmailField(verbose_name='email',unique=True,null=True,max_length=60)
    username=models.CharField(max_length=50,unique=True,null=True)
    first_name=models.CharField(max_length=60,null=True)
    last_name=models.CharField(max_length=60,null=True)
    other_names=models.CharField(max_length=60,null=True)
    phone_number=models.CharField(max_length=11,null=True)
    profile_picture=models.ImageField(null=True,blank=True,upload_to='proile_pics/')
    date_joined=models.DateTimeField(null=True, blank=True,auto_now_add=True,verbose_name='date joined')
    last_login=models.DateTimeField(null=True,auto_now=True,)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    pharmacys=models.ManyToManyField("main.Pharmacy",related_name="admin")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']