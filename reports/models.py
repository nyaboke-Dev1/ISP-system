from django.db import models
from accounts.models import User
from subscriptions.models import Subscription


class UsageRecord(models.Model):
    """Track customer bandwidth usage"""
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage_records')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage_records')
    date = models.DateField()
    download_bytes = models.BigIntegerField(default=0)
    upload_bytes = models.BigIntegerField(default=0)
    session_time = models.IntegerField(default=0, help_text="Session time in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usage_records'
        ordering = ['-date']
        unique_together = ['customer', 'subscription', 'date']
        verbose_name = 'Usage Record'
        verbose_name_plural = 'Usage Records'
    
    def __str__(self):
        return f"{self.customer.get_full_name()} - {self.date}"
    
    @property
    def total_gb(self):
        """Total usage in GB"""
        return (self.download_bytes + self.upload_bytes) / (1024**3)
    
    @property
    def download_gb(self):
        """Download usage in GB"""
        return self.download_bytes / (1024**3)
    
    @property
    def upload_gb(self):
        """Upload usage in GB"""
        return self.upload_bytes / (1024**3)
    
    @property
    def session_hours(self):
        """Session time in hours"""
        return self.session_time / 3600