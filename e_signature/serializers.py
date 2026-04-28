from rest_framework import serializers

from accounts.models import User
from documents.models import Document
from e_signature.models import SignatureAuditTrail, SignatureParty, SignatureRequest, SignedDocument
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class SignatureRequestSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    document_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'document_id': Document}

    class Meta:
        model = SignatureRequest
        fields = [
            'id', 'organization', 'organization_id', 'document', 'document_id',
            'title', 'requested_by', 'status', 'created_at',
        ]
        read_only_fields = ['organization', 'document', 'requested_by', 'created_at']

    def create(self, validated_data):
        return SignatureRequest.objects.create(
            organization_id=validated_data['organization_id'],
            document_id=validated_data.get('document_id'),
            title=validated_data['title'],
            requested_by=self.context['request'].user,
            status=validated_data.get('status', 'draft'),
        )


class SignaturePartySerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    signature_request_id = serializers.UUIDField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'signature_request_id': SignatureRequest, 'user_id': User}

    class Meta:
        model = SignatureParty
        fields = [
            'id', 'organization', 'organization_id', 'signature_request', 'signature_request_id',
            'user', 'user_id', 'status', 'created_at',
        ]
        read_only_fields = ['organization', 'signature_request', 'user', 'created_at']

    def create(self, validated_data):
        return SignatureParty.objects.create(
            organization_id=validated_data['organization_id'],
            signature_request_id=validated_data['signature_request_id'],
            user_id=validated_data['user_id'],
            status=validated_data.get('status', 'pending'),
        )


class SignedDocumentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    signature_request_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'signature_request_id': SignatureRequest}

    class Meta:
        model = SignedDocument
        fields = [
            'id', 'organization', 'organization_id', 'signature_request',
            'signature_request_id', 'signed_at', 'created_at',
        ]
        read_only_fields = ['organization', 'signature_request', 'created_at']

    def create(self, validated_data):
        return SignedDocument.objects.create(
            organization_id=validated_data['organization_id'],
            signature_request_id=validated_data['signature_request_id'],
            signed_at=validated_data.get('signed_at'),
        )


class SignatureAuditTrailSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    signature_request_id = serializers.UUIDField(write_only=True)
    actor_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'signature_request_id': SignatureRequest, 'actor_id': User}

    class Meta:
        model = SignatureAuditTrail
        fields = [
            'id', 'organization', 'organization_id', 'signature_request', 'signature_request_id',
            'actor', 'actor_id', 'event', 'metadata', 'created_at',
        ]
        read_only_fields = ['organization', 'signature_request', 'actor', 'created_at']

    def create(self, validated_data):
        return SignatureAuditTrail.objects.create(
            organization_id=validated_data['organization_id'],
            signature_request_id=validated_data['signature_request_id'],
            actor_id=validated_data.get('actor_id'),
            event=validated_data['event'],
            metadata=validated_data.get('metadata', {}),
        )
