from django.contrib import admin
from .models import Subscription
from datetime import timedelta


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'status', 'start_date', 'next_billing_date', 'auto_renew']
    list_filter = ['status', 'auto_renew', 'package']
    search_fields = ['user__username', 'user__account_number']
    date_hierarchy = 'start_date'
