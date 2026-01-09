from django.contrib import admin
from .models import UsageRecord


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date', 'download_display', 'upload_display', 'total_display']
    list_filter = ['date']
    search_fields = ['customer__username']
    date_hierarchy = 'date'
    
    def download_display(self, obj):
        return f"{obj.download_gb:.2f} GB"
    
    def upload_display(self, obj):
        return f"{obj.upload_gb:.2f} GB"
    
    def total_display(self, obj):
        return f"{obj.total_gb:.2f} GB"