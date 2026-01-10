from django.db import models
from accounts.models import User
from packages.models import Package


class Subscription(models.Model):
    """Customer subscriptions to service plans"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("cancelled", "Cancelled"),
        ("pending", "Pending Activation"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    package = models.ForeignKey(
        Package, on_delete=models.PROTECT, related_name="subscriptions"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_billing_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    installation_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"
        ordering = ["-created_at"]
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.package.name}"

    @property
    def is_active(self):
        """Check if subscription is active"""
        return self.status == "active"
