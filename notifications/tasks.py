from celery import shared_task
from notifications.services import NotificationService
from notifications.models import Notification
from django.utils import timezone


@shared_task
def send_pending_notifications():
    pending = Notification.objects.filter(sent=False)
    service = NotificationService()
    for notification in pending:
        if notification.channel == 'email':
            service.send_email(
                subject=notification.subject,
                message=notification.body,
                recipient_list=[notification.recipient],
            )
        else:
            service.send_whatsapp(
                organization_id=notification.organization_id,
                recipient=notification.recipient,
                body=notification.body,
                notification=notification,
            )
        if not notification.sent:
            notification.sent = True
            notification.sent_at = timezone.now()
            notification.save()
