from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, SupportTicket, TicketComment


@admin.register(User)
class CustomerAdmin(UserAdmin):
    list_display = ['username', 'email', 'get_full_name', 'account_number', 'phone', 'is_active_customer', 'date_joined']
    list_filter = ['is_active_customer', 'date_joined', 'city']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'account_number', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Customer Information', {
            'fields': ('phone', 'address', 'city', 'postal_code', 'installation_address', 'account_number', 'is_active_customer')
        }),
    )


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1
    fields = ['author', 'comment', 'is_internal', 'created_at']
    readonly_fields = ['created_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'subject', 'category', 'priority_display', 'status', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'subject', 'user__username']
    inlines = [TicketCommentInline]
    
    def priority_display(self, obj):
        colors = {'urgent': 'red', 'high': 'orange', 'medium': 'blue', 'low': 'green'}
        return format_html('<span style="color: {};">{}</span>', colors.get(obj.priority), obj.get_priority_display())