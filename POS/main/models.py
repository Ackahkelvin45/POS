from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from authentication.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage




class Domain(DomainMixin):
    pass

class Pharmacy(TenantMixin):
    name = models.CharField(max_length=100,null=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    schema_name = models.CharField(max_length=63, unique=True, db_index=True,null=True)
    owner = models.ForeignKey(User, related_name="tenant_admin", on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, null=True)
    is_mainbranch = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True)
    workers = models.ManyToManyField(User, related_name="pharmacy_working")
   

   
    
    auto_create_schema = True

    #send email when account is verified 
    def send_verification_email(self):
        domain=Domain.objects.get(tenant_id=self.pk)
        template = render_to_string("main/email_message.html", {"name":self.owner.first_name,"url":domain.domain})
        email = EmailMessage(
        "Thank you for choosing samsoft pharmacies!",
        template,
        settings.EMAIL_HOST_USER,
        [self.owner.email]
                )
        email.fail_silently = False
        email.send()
        
    def save_with_default_behavior(self, *args, **kwargs):
        super(Pharmacy, self).save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if self.pk is not None:
            
            if self.is_verified:
                self.send_verification_email()

        super().save(*args, **kwargs)

  

   
