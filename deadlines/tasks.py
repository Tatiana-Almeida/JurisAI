from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from deadlines.models import Deadline
from notifications.services import NotificationService

@shared_task
def send_deadline_reminders():
    now = timezone.now()
    soon = now + timezone.timedelta(hours=24)
    deadlines = Deadline.objects.filter(due_date__lte=soon, completed=False)
    for deadline in deadlines:
        case = deadline.law_case
        message = f'Reminder: prazo para o processo "{case.title}" vence em {deadline.due_date.strftime("%Y-%m-%d %H:%M")}'
        NotificationService().send_email(
            subject='Alerta de prazo jurídico',
            message=message,
            recipient_list=[case.lawyer.email],
        )
