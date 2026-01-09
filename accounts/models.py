from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
from django.dispatch import receiver 
from django.db.models.signals import post_save


class User(AbstractUser):
    """Extended user model for ISP system"""
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )
    
    # Additional customer fields
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    account_number = models.CharField(max_length=20, unique=True, blank=True)
    is_active_customer = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Auto-generate account number if not exists
        if not self.account_number:
            self.account_number = f"ISP{timezone.now().strftime('%Y%m')}{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
    
    def get_full_name(self):
        """Return the full name of the user"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class SupportTicket(models.Model):
    """Customer support tickets"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting', 'Waiting for Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'Technical Issue'),
        ('billing', 'Billing'),
        ('account', 'Account Management'),
        ('installation', 'Installation'),
        ('other', 'Other'),
    ]
    
    ticket_number = models.CharField(max_length=50, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tickets',
        limit_choices_to={'role': 'ADMIN'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'
    
    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{timezone.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)


class TicketComment(models.Model):
    """Comments on support tickets"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    is_internal = models.BooleanField(default=False, help_text="Internal notes not visible to customer")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ticket_comments'
        ordering = ['created_at']
        verbose_name = 'Ticket Comment'
        verbose_name_plural = 'Ticket Comments'
    
    def __str__(self):
        return f"Comment on {self.ticket.ticket_number} by {self.author.username}"
    
class Profile(models.Model):   
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# blogs = models.ManyToManyField(Blog)

	@receiver(post_save, sender=User) #add this
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User) #add this
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
    
# from django.db import models
# from django.contrib.auth.models import AbstractUser

# # Create your models here.

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('ADMIN', 'Admin'),
#         ('CUSTOMER', 'Customer'),
#     )
#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='CUSTOMER'
#     )

#     def __str__(self):
#         return self.username
