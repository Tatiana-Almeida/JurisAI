from django.contrib import admin
from notifications.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'channel', 'sent', 'created_at', 'sent_at')
    list_filter = ('channel', 'sent')
    search_fields = ('recipient', 'body')
