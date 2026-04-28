from rest_framework import serializers
from billing.models import Payment, Subscription, Invoice
from jurisai.serializers import OrganizationScopedValidationMixin


class PaymentSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Payment
        fields = ['id', 'organization', 'organization_id', 'amount', 'status', 'method', 'created_at', 'updated_at']
        read_only_fields = ['organization', 'created_at', 'updated_at']

    def create(self, validated_data, **kwargs):
        return Payment.objects.create(
            organization_id=validated_data['organization_id'],
            amount=validated_data['amount'],
            status=validated_data.get('status', 'pending'),
            method=validated_data['method'],
        )


class SubscriptionSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Subscription
        fields = ['id', 'organization', 'organization_id', 'stripe_subscription_id', 'plan', 'status', 'current_period_start', 'current_period_end', 'trial_end', 'created_at', 'updated_at']
        read_only_fields = ['organization', 'created_at', 'updated_at']

    def create(self, validated_data, **kwargs):
        return Subscription.objects.create(
            organization_id=validated_data['organization_id'],
            stripe_subscription_id=validated_data['stripe_subscription_id'],
            plan=validated_data['plan'],
            status=validated_data.get('status', 'active'),
            current_period_start=validated_data.get('current_period_start'),
            current_period_end=validated_data.get('current_period_end'),
            trial_end=validated_data.get('trial_end'),
        )


class InvoiceSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Invoice
        fields = ['id', 'organization', 'organization_id', 'stripe_invoice_id', 'amount', 'status', 'due_date', 'paid_at', 'created_at', 'updated_at']
        read_only_fields = ['organization', 'created_at', 'updated_at']

    def create(self, validated_data, **kwargs):
        return Invoice.objects.create(
            organization_id=validated_data['organization_id'],
            stripe_invoice_id=validated_data['stripe_invoice_id'],
            amount=validated_data['amount'],
            status=validated_data.get('status', 'open'),
            due_date=validated_data.get('due_date'),
            paid_at=validated_data.get('paid_at'),
        )
