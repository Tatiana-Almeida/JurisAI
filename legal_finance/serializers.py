from rest_framework import serializers

from accounts.models import User
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from law_cases.models import LawCase
from legal_finance.models import ClientInvoice, Expense, LegalFee, PaymentRecord


class ClientInvoiceSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    client_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {
        'law_case_id': LawCase,
        'client_id': User,
    }

    class Meta:
        model = ClientInvoice
        fields = ['id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'client', 'client_id', 'invoice_number', 'description', 'amount', 'status', 'issued_at', 'due_date', 'paid_at', 'created_at']
        read_only_fields = ['organization', 'law_case', 'client', 'created_at']

    def create(self, validated_data):
        return ClientInvoice.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            client_id=validated_data.get('client_id'),
            invoice_number=validated_data['invoice_number'],
            description=validated_data.get('description', ''),
            amount=validated_data['amount'],
            status=validated_data.get('status', 'draft'),
            issued_at=validated_data.get('issued_at'),
            due_date=validated_data.get('due_date'),
            paid_at=validated_data.get('paid_at'),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['client_id'] = str(instance.client_id) if instance.client_id else None
        return data


class LegalFeeSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    client_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {
        'law_case_id': LawCase,
        'client_id': User,
    }

    class Meta:
        model = LegalFee
        fields = ['id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'client', 'client_id', 'fee_type', 'description', 'amount', 'currency', 'status', 'created_at']
        read_only_fields = ['organization', 'law_case', 'client', 'created_at']

    def create(self, validated_data):
        return LegalFee.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            client_id=validated_data.get('client_id'),
            fee_type=validated_data.get('fee_type', 'fixed'),
            description=validated_data.get('description', ''),
            amount=validated_data['amount'],
            currency=validated_data.get('currency', 'AOA'),
            status=validated_data.get('status', 'pending'),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['client_id'] = str(instance.client_id) if instance.client_id else None
        return data


class ExpenseSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    created_by_id = serializers.UUIDField(source='created_by.id', read_only=True)
    tenant_relation_fields = {
        'law_case_id': LawCase,
    }

    class Meta:
        model = Expense
        fields = ['id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'description', 'amount', 'currency', 'expense_date', 'reimbursable', 'created_by', 'created_by_id', 'created_at']
        read_only_fields = ['organization', 'law_case', 'created_by', 'created_at']

    def create(self, validated_data):
        return Expense.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            description=validated_data['description'],
            amount=validated_data['amount'],
            currency=validated_data.get('currency', 'AOA'),
            expense_date=validated_data['expense_date'],
            reimbursable=validated_data.get('reimbursable', False),
            created_by=self.context['request'].user,
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['created_by_id'] = str(instance.created_by_id)
        return data


class PaymentRecordSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    invoice_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {
        'invoice_id': ClientInvoice,
        'law_case_id': LawCase,
    }

    class Meta:
        model = PaymentRecord
        fields = ['id', 'organization', 'organization_id', 'invoice', 'invoice_id', 'law_case', 'law_case_id', 'amount', 'currency', 'payment_method', 'paid_at', 'reference', 'created_at']
        read_only_fields = ['organization', 'invoice', 'law_case', 'created_at']

    def create(self, validated_data):
        return PaymentRecord.objects.create(
            organization_id=validated_data['organization_id'],
            invoice_id=validated_data.get('invoice_id'),
            law_case_id=validated_data.get('law_case_id'),
            amount=validated_data['amount'],
            currency=validated_data.get('currency', 'AOA'),
            payment_method=validated_data.get('payment_method', 'other'),
            paid_at=validated_data['paid_at'],
            reference=validated_data.get('reference', ''),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['invoice_id'] = str(instance.invoice_id) if instance.invoice_id else None
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        return data
