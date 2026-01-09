from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.timezone import now

class Package(models.Model):
    """Internet service packages/plans"""
    PLAN_TYPES = [
        ('home', 'Home'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='home')
    
    # Use DecimalField for money (more accurate than FloatField)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    setup_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    # Speed fields (in Mbps)
    speed = models.IntegerField(default=10, help_text="Download speed in Mbps")  # Keep your field name
    upload_speed = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Upload speed in Mbps. If not set, assumed symmetric with download."
    )
    
    # Data cap
    data_cap = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Data cap in GB. Leave blank for unlimited."
    )
    
    duration = models.IntegerField(default=30, help_text="Duration in days")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'packages'
        ordering = ['price']
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
    
    def __str__(self):
        return f"{self.name} - {self.speed}Mbps - ${self.price}"
    
    @property
    def speed_display(self):
        """Return formatted speed display"""
        upload = self.upload_speed or self.speed  # Use download speed if upload not set
        return f"↓{self.speed} Mbps / ↑{upload} Mbps"
    
    @property
    def data_cap_display(self):
        """Return formatted data cap"""
        if self.data_cap:
            return f"{self.data_cap} GB"
        return "Unlimited"
    
    @property
    def monthly_price(self):
        """Alias for price to match our original design"""
        return self.price