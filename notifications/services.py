from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from notifications.models import Notification


class NotificationService:
    def send_email(self, subject: str, message: str, recipient_list: list[str]):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

    def send_whatsapp(self, organization_id, recipient: str, body: str, notification=None):
        # Preserve the legacy mock behavior unless a pending notification is explicitly reused.
        if notification is None:
            Notification.objects.create(
                organization_id=organization_id,
                channel='whatsapp',
                recipient=recipient,
                subject='WhatsApp',
                body=body,
                sent=True,
                sent_at=timezone.now(),
            )
            return

        notification.sent = True
        notification.sent_at = timezone.now()
        notification.save(update_fields=['sent', 'sent_at'])
