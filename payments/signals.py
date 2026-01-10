from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


@receiver(post_save, sender=Payment)
def activate_subscription(sender, instance, created, **kwargs):
    if instance.status == "completed":
        subscription = instance.subscription
        if subscription.status != "active":
            subscription.status = "active"
            subscription.save()
