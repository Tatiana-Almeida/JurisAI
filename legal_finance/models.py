import uuid

from django.conf import settings
from django.db import models


class ClientInvoice(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('overdue', 'Overdue'), ('cancelled', 'Cancelled')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='client_invoices')
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='client_invoices', null=True, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='client_invoices', null=True, blank=True)
    invoice_number = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issued_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'invoice_number')


class LegalFee(models.Model):
    FEE_TYPE_CHOICES = [('fixed', 'Fixed'), ('hourly', 'Hourly'), ('retainer', 'Retainer'), ('success', 'Success'), ('other', 'Other')]
    STATUS_CHOICES = [('pending', 'Pending'), ('partially_paid', 'Partially Paid'), ('paid', 'Paid'), ('cancelled', 'Cancelled')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='legal_fees')
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='legal_fees', null=True, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='legal_fees', null=True, blank=True)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='fixed')
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='AOA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='expenses')
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='expenses', null=True, blank=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='AOA')
    expense_date = models.DateTimeField()
    reimbursable = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentRecord(models.Model):
    PAYMENT_METHOD_CHOICES = [('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('card', 'Card'), ('multicaixa', 'Multicaixa'), ('other', 'Other')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, related_name='legal_finance_payments')
    invoice = models.ForeignKey('legal_finance.ClientInvoice', on_delete=models.PROTECT, related_name='payments', null=True, blank=True)
    law_case = models.ForeignKey('law_cases.LawCase', on_delete=models.PROTECT, related_name='payment_records', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='AOA')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='other')
    paid_at = models.DateTimeField()
    reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

