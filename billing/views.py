import json

from django.conf import settings
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from billing.models import Payment, Subscription, Invoice
from billing.services import (
    get_webhook_event_id,
    get_webhook_event_object,
    get_webhook_event_type,
    parse_webhook_payload,
    process_billing_webhook_event,
    resolve_webhook_organization,
    validate_stripe_timestamp,
    verify_stripe_signature,
)
from billing.serializers import PaymentSerializer, SubscriptionSerializer, InvoiceSerializer
from jurisai.permissions import IsOrganizationMember


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('organization').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'method']
    ordering_fields = ['created_at', 'amount']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related('organization').all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'plan']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('organization').all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['due_date', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        secret = settings.STRIPE_WEBHOOK_SECRET
        tolerance_seconds = settings.STRIPE_WEBHOOK_TOLERANCE_SECONDS
        signature = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        payload_body = request.body

        if not secret:
            return Response({'detail': 'Webhook signature validation is not configured.'}, status=status.HTTP_400_BAD_REQUEST)

        if not signature:
            return Response({'detail': 'Missing Stripe signature.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_stripe_signature(payload_body, signature, secret):
            return Response({'detail': 'Invalid Stripe signature.'}, status=status.HTTP_400_BAD_REQUEST)

        is_fresh, signature_timestamp = validate_stripe_timestamp(signature, tolerance_seconds)
        if not is_fresh:
            return Response({'detail': 'Expired or invalid Stripe timestamp.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = parse_webhook_payload(payload_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return Response({'detail': 'Invalid webhook payload.'}, status=status.HTTP_400_BAD_REQUEST)

        event_type = get_webhook_event_type(event)
        event_id = get_webhook_event_id(event)
        payload = get_webhook_event_object(event)
        if not event_type or not event_id or not isinstance(payload, dict):
            return Response({'detail': 'Invalid webhook payload.'}, status=status.HTTP_400_BAD_REQUEST)

        organization = resolve_webhook_organization(payload)

        if event_type == 'invoice.payment_succeeded' and organization and payload.get('amount_paid') is None:
            return Response({'detail': 'Invalid webhook payload.'}, status=status.HTTP_400_BAD_REQUEST)

        if event_type == 'invoice.payment_failed' and organization and payload.get('amount_due') is None:
            return Response({'detail': 'Invalid webhook payload.'}, status=status.HTTP_400_BAD_REQUEST)

        if event_type == 'customer.subscription.updated' and organization:
            subscription_id = payload.get('id')
            subscription_status = payload.get('status')
            if not subscription_id or not subscription_status:
                return Response({'detail': 'Invalid webhook payload.'}, status=status.HTTP_400_BAD_REQUEST)
        result = process_billing_webhook_event(
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            payload_body=payload_body,
            signature_timestamp=signature_timestamp,
            organization=organization,
            subscription_id=subscription_id if event_type == 'customer.subscription.updated' and organization else None,
            subscription_status=subscription_status if event_type == 'customer.subscription.updated' and organization else None,
        )

        return Response({'received': True, 'event_type': result.event_type}, status=status.HTTP_200_OK)
