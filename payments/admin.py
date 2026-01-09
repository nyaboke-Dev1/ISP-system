from django.contrib import admin
from .models import Payment
# Register your models here.
# admin.site.register(Payment)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscription',
        'amount',
        'method',
        'status',
        'timestamp',
    )

    list_filter = (
        'status',
        'method',
        'timestamp',
    )

    search_fields = (
        'user__username',
        'user__email',
        'subscription__id',
    )

    ordering = ('-timestamp',)

    readonly_fields = (
        'timestamp',
    )

    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'subscription', 'amount')
        }),
        ('Status & Method', {
            'fields': ('status', 'method')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )

