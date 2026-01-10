from django.db import models
from django.conf import settings
from subscriptions.models import Subscription
from decimal import Decimal


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_METHODS = [
        ("mpesa", "MPesa"),
        ("card", "Card"),
        ("bank", "Bank Transfer"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments"
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="mpesa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    # M-Pesa specific fields
    mpesa_receipt_number = models.CharField(max_length=20, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=50, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} KES ({self.status})"
