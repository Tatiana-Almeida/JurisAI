from django.contrib import admin
from audit_logs.models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'entity', 'user', 'timestamp')
    search_fields = ('entity', 'action', 'before', 'after')
    list_filter = ('action',)
