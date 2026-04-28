from celery import shared_task
from django.utils import timezone
from billing.models import Invoice
from notifications.services import NotificationService

@shared_task
def process_recurring_charges():
    now = timezone.now()
    overdue_invoices = Invoice.objects.filter(status='open', due_date__lte=now)
    service = NotificationService()
    for invoice in overdue_invoices:
        invoice.status = 'past_due'
        invoice.save()
        admin_emails = [user.email for user in invoice.organization.users.filter(role='admin')]
        if admin_emails:
            service.send_email(
                subject='Fatura em atraso',
                message=f'Sua fatura {invoice.stripe_invoice_id} está em atraso. Por favor quite o valor de R${invoice.amount}.',
                recipient_list=admin_emails,
            )
