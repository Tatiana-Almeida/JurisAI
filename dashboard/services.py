from django.db.models import Count
from django.utils import timezone

from deadlines.models import Deadline
from documents.models import Document
from law_cases.models import LawCase
from legal_finance.models import ClientInvoice
from tasks.models import Task


def get_dashboard_summary(organization):
    now = timezone.now()
    return {
        'total_cases': LawCase.objects.filter(organization=organization, deleted=False).count(),
        'active_cases': LawCase.objects.filter(organization=organization, deleted=False, status__in=['open', 'in_progress']).count(),
        'total_documents': Document.objects.filter(organization=organization).count(),
        'upcoming_deadlines': Deadline.objects.filter(organization=organization, completed=False, due_date__gte=now).count(),
        'overdue_deadlines': Deadline.objects.filter(organization=organization, completed=False, due_date__lt=now).count(),
        'pending_tasks': Task.objects.filter(organization=organization, is_deleted=False, status__in=['pending', 'in_progress', 'blocked']).count(),
        'completed_tasks': Task.objects.filter(organization=organization, is_deleted=False, status='completed').count(),
        'pending_invoices': ClientInvoice.objects.filter(organization=organization, status__in=['draft', 'open', 'overdue']).count(),
    }


def get_upcoming_deadlines(organization):
    return Deadline.objects.filter(organization=organization, completed=False).order_by('due_date')[:10]


def get_dashboard_tasks(organization):
    return Task.objects.filter(organization=organization, is_deleted=False).order_by('due_date', '-created_at')[:10]


def get_dashboard_documents(organization):
    return Document.objects.filter(organization=organization).order_by('-created_at')[:10]


def get_dashboard_financial(organization):
    invoices = ClientInvoice.objects.filter(organization=organization)
    return {
        'pending_invoices': invoices.filter(status__in=['draft', 'open', 'overdue']).count(),
        'paid_invoices': invoices.filter(status='paid').count(),
        'overdue_invoices': invoices.filter(status='overdue').count(),
    }

