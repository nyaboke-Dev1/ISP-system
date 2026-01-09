from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

from .models import Subscription


@receiver(pre_save, sender=Subscription)
def set_end_date(sender, instance, **kwargs):
    """
    Automatically set subscription end date based on package duration.
    """
    # If package exists and end_date not yet set
    if instance.package_id and not instance.end_date:
        # start_date may not exist yet on first save
        start_date = instance.start_date or timezone.now()
        instance.end_date = start_date + timedelta(days=instance.package.duration)
