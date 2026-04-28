from rest_framework import serializers

from accounts.models import User
from client_portal.models import ClientCaseVisibility, ClientDocumentShare, ClientMessage, ClientPortalAccess
from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from law_cases.models import LawCase


class ClientPortalAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPortalAccess
        fields = '__all__'


class ClientCaseVisibilitySerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    client_id = serializers.UUIDField(write_only=True)
    law_case_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {
        'client_id': User,
        'law_case_id': LawCase,
    }

    class Meta:
        model = ClientCaseVisibility
        fields = ['id', 'organization', 'organization_id', 'client', 'client_id', 'law_case', 'law_case_id', 'can_view', 'created_at']
        read_only_fields = ['organization', 'client', 'law_case', 'created_at']

    def create(self, validated_data):
        return ClientCaseVisibility.objects.create(
            organization_id=validated_data['organization_id'],
            client_id=validated_data['client_id'],
            law_case_id=validated_data['law_case_id'],
            can_view=validated_data.get('can_view', True),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['client_id'] = str(instance.client_id)
        data['law_case_id'] = str(instance.law_case_id)
        return data


class ClientDocumentShareSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    client_id = serializers.UUIDField(write_only=True)
    document_id = serializers.UUIDField(write_only=True)
    shared_by_id = serializers.UUIDField(source='shared_by.id', read_only=True)
    tenant_relation_fields = {
        'client_id': User,
        'document_id': Document,
    }

    class Meta:
        model = ClientDocumentShare
        fields = ['id', 'organization', 'organization_id', 'client', 'client_id', 'document', 'document_id', 'shared_by', 'shared_by_id', 'can_download', 'expires_at', 'created_at']
        read_only_fields = ['organization', 'client', 'document', 'shared_by', 'created_at']

    def create(self, validated_data):
        return ClientDocumentShare.objects.create(
            organization_id=validated_data['organization_id'],
            client_id=validated_data['client_id'],
            document_id=validated_data['document_id'],
            shared_by=self.context['request'].user,
            can_download=validated_data.get('can_download', True),
            expires_at=validated_data.get('expires_at'),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['client_id'] = str(instance.client_id)
        data['document_id'] = str(instance.document_id)
        data['shared_by_id'] = str(instance.shared_by_id)
        return data


class ClientMessageSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    recipient_id = serializers.UUIDField(write_only=True)
    sender_id = serializers.UUIDField(source='sender.id', read_only=True)
    tenant_relation_fields = {
        'law_case_id': LawCase,
        'recipient_id': User,
    }

    class Meta:
        model = ClientMessage
        fields = ['id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'sender', 'sender_id', 'recipient', 'recipient_id', 'message', 'is_read', 'created_at']
        read_only_fields = ['organization', 'law_case', 'sender', 'recipient', 'is_read', 'created_at']

    def create(self, validated_data):
        return ClientMessage.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            sender=self.context['request'].user,
            recipient_id=validated_data['recipient_id'],
            message=validated_data['message'],
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['sender_id'] = str(instance.sender_id)
        data['recipient_id'] = str(instance.recipient_id)
        return data
