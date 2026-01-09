from django.contrib import admin
from django.utils.html import format_html
from .models import Package


@admin.register(Package)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'speed_display', 'data_cap_display', 'monthly_price', 'is_active', 'subscriber_count']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    def speed_display(self, obj):
        return f"↓{obj.download_speed} / ↑{obj.upload_speed} Mbps"
    speed_display.short_description = 'Speed'
    
    def data_cap_display(self, obj):
        return f"{obj.data_cap} GB" if obj.data_cap else "Unlimited"
    data_cap_display.short_description = 'Data Cap'
    
    def subscriber_count(self, obj):
        count = obj.subscriptions.filter(status='active').count()
        return format_html('<strong>{}</strong>', count)
    subscriber_count.short_description = 'Active Subscribers'