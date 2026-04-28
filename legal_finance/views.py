from django.db.models import Sum
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from jurisai.permissions import IsOrganizationMember
from legal_finance.models import ClientInvoice, Expense, LegalFee, PaymentRecord
from legal_finance.serializers import ClientInvoiceSerializer, ExpenseSerializer, LegalFeeSerializer, PaymentRecordSerializer


class OrganizationFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        organization = getattr(self.request.user, 'organization', None)
        return super().get_queryset().filter(organization=organization) if organization else super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class ClientInvoiceViewSet(OrganizationFilteredViewSet):
    queryset = ClientInvoice.objects.select_related('organization', 'law_case', 'client').all()
    serializer_class = ClientInvoiceSerializer
    filterset_fields = ['status', 'law_case_id', 'client_id']
    search_fields = ['invoice_number', 'description']
    ordering_fields = ['created_at', 'due_date', 'issued_at']


class LegalFeeViewSet(OrganizationFilteredViewSet):
    queryset = LegalFee.objects.select_related('organization', 'law_case', 'client').all()
    serializer_class = LegalFeeSerializer
    filterset_fields = ['status', 'fee_type', 'law_case_id', 'client_id']
    search_fields = ['description']
    ordering_fields = ['created_at']


class ExpenseViewSet(OrganizationFilteredViewSet):
    queryset = Expense.objects.select_related('organization', 'law_case', 'created_by').all()
    serializer_class = ExpenseSerializer
    filterset_fields = ['reimbursable', 'law_case_id']
    search_fields = ['description']
    ordering_fields = ['created_at', 'expense_date']


class PaymentRecordViewSet(OrganizationFilteredViewSet):
    queryset = PaymentRecord.objects.select_related('organization', 'invoice', 'law_case').all()
    serializer_class = PaymentRecordSerializer
    filterset_fields = ['payment_method', 'invoice_id', 'law_case_id']
    search_fields = ['reference']
    ordering_fields = ['created_at', 'paid_at']


class LegalFinanceSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        organization = request.user.organization
        invoices = ClientInvoice.objects.filter(organization=organization)
        payments = PaymentRecord.objects.filter(organization=organization)
        expenses = Expense.objects.filter(organization=organization)
        return Response({
            'total_invoices': invoices.count(),
            'open_invoices': invoices.filter(status__in=['draft', 'open', 'overdue']).count(),
            'paid_invoices': invoices.filter(status='paid').count(),
            'total_payments': payments.count(),
            'payments_amount': payments.aggregate(total=Sum('amount'))['total'] or 0,
            'expenses_amount': expenses.aggregate(total=Sum('amount'))['total'] or 0,
        })

