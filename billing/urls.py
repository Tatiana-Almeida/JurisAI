from django.urls import path, include
from rest_framework.routers import DefaultRouter
from billing.views import PaymentViewSet, SubscriptionViewSet, InvoiceViewSet, StripeWebhookView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', StripeWebhookView.as_view(), name='billing_webhook'),
]
