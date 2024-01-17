from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_tenants.utils import get_tenant

def create_admin_group(pharmacy):

    admin_group = Group.objects.create(custom_name='Administrator')
    
    all_permissions = Permission.objects.all()

    admin_group.permissions.set(all_permissions)
    admin_group.pharmacy = pharmacy.name
    admin_group.save()


    return admin_group.id 



def send_verification_email(user):
    template = render_to_string("auth/email_message.html", {"name": user.first_name})
    email = EmailMessage(
        "Thank you for choosing samsof pharmacies!",
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.fail_silently = False
    email.send()