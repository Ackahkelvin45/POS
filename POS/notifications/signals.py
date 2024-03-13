from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from main.models import Pharmacy
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Pharmacy)
def send_signup_notification(sender, instance, created, **kwargs):
    if created and instance.is_verified:
        channel_layer = get_channel_layer()
        group_name = 'user-notifications'
        event = {
            'type': 'user_verified',
            'text': instance.name,
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
        