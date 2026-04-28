from django.contrib import admin
from billing.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('organization', 'amount', 'status', 'method', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('organization__name',)
