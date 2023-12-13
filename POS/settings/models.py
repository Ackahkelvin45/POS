from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class EmailBackend(models.Model):
    email = models.EmailField(verbose_name="pharmacy_email", max_length=255, null=True)
    email_host = models.CharField(max_length=255, null=True, blank=True)
    email_port = models.CharField(max_length=10, null=True, blank=True)
    email_host_password = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.email

        
    def save(self, *args, **kwargs):
            # Check if the email contains "gmail," "yahoo," or "outlook"
            if 'gmail' in self.email:
                self.email_host = 'smtp.gmail.com'
                self.email_port = '587'  # Update with the correct port for Gmail
            elif 'yahoo' in self.email:
                self.email_host = 'smtp.mail.yahoo.com'
                self.email_port = '587'  # Update with the correct port for Yahoo
            elif 'outlook' in self.email:
                self.email_host = 'smtp.office365.com'
                self.email_port = '587'  # Update with the correct port for Outlook
            else:
                #
                raise ValidationError("This email provider is not supported. Please use Gmail, Yahoo, or Outlook.")
            
            
            super(EmailBackend, self).save(*args, **kwargs)   





    

class AppSettings(models.Model):
    automatic_print_receipt = models.BooleanField(default=False)
    allow_date_change = models.BooleanField(default=True)
    allow_typeahead=models.BooleanField(default=True)