from django.urls import include, path
from rest_framework.routers import DefaultRouter

from legal_finance.views import (
    ClientInvoiceViewSet,
    ExpenseViewSet,
    LegalFeeViewSet,
    LegalFinanceSummaryView,
    PaymentRecordViewSet,
)


router = DefaultRouter()
router.register(r'invoices', ClientInvoiceViewSet, basename='legal-finance-invoice')
router.register(r'fees', LegalFeeViewSet, basename='legal-finance-fee')
router.register(r'expenses', ExpenseViewSet, basename='legal-finance-expense')
router.register(r'payments', PaymentRecordViewSet, basename='legal-finance-payment')

urlpatterns = [
    path('summary/', LegalFinanceSummaryView.as_view()),
    path('', include(router.urls)),
]

