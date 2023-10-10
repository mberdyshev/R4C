from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.views import send_email_awaiting
from robots.models import Robot


@receiver(post_save, sender=Robot, dispatch_uid='send_email_to_customers')
def send_email_to_customers(sender, **kwargs):
    if kwargs['raw']:
        return
    send_email_awaiting(kwargs['instance'].serial)
