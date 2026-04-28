from rest_framework import serializers

from accounts.models import User
from compliance.models import (
    AccessLog,
    DataConsent,
    DataDeletionRequest,
    DataExportRequest,
    DataRetentionPolicy,
    SensitiveDataFlag,
)
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class DataConsentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    user_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'user_id': User}

    class Meta:
        model = DataConsent
        fields = ['id', 'organization', 'organization_id', 'user', 'user_id', 'purpose', 'granted', 'granted_at']
        read_only_fields = ['organization', 'user', 'granted_at']

    def create(self, validated_data):
        return DataConsent.objects.create(
            organization_id=validated_data['organization_id'],
            user_id=validated_data['user_id'],
            purpose=validated_data['purpose'],
            granted=validated_data.get('granted', True),
        )


class DataRetentionPolicySerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = DataRetentionPolicy
        fields = ['id', 'organization', 'organization_id', 'name', 'retention_days', 'is_active', 'created_at']
        read_only_fields = ['organization', 'created_at']

    def create(self, validated_data):
        return DataRetentionPolicy.objects.create(
            organization_id=validated_data['organization_id'],
            name=validated_data['name'],
            retention_days=validated_data.get('retention_days', 0),
            is_active=validated_data.get('is_active', True),
        )


class SensitiveDataFlagSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = SensitiveDataFlag
        fields = ['id', 'organization', 'organization_id', 'resource_type', 'resource_id', 'reason', 'created_at']
        read_only_fields = ['organization', 'created_at']

    def create(self, validated_data):
        return SensitiveDataFlag.objects.create(
            organization_id=validated_data['organization_id'],
            resource_type=validated_data['resource_type'],
            resource_id=validated_data['resource_id'],
            reason=validated_data['reason'],
        )


class DataExportRequestSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = DataExportRequest
        fields = ['id', 'organization', 'organization_id', 'requested_by', 'status', 'created_at']
        read_only_fields = ['organization', 'requested_by', 'created_at']

    def create(self, validated_data):
        return DataExportRequest.objects.create(
            organization_id=validated_data['organization_id'],
            requested_by=self.context['request'].user,
            status=validated_data.get('status', 'pending'),
        )


class DataDeletionRequestSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = DataDeletionRequest
        fields = ['id', 'organization', 'organization_id', 'requested_by', 'reason', 'status', 'created_at']
        read_only_fields = ['organization', 'requested_by', 'created_at']

    def create(self, validated_data):
        return DataDeletionRequest.objects.create(
            organization_id=validated_data['organization_id'],
            requested_by=self.context['request'].user,
            reason=validated_data.get('reason', ''),
            status=validated_data.get('status', 'pending'),
        )


class AccessLogSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    user_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'user_id': User}

    class Meta:
        model = AccessLog
        fields = ['id', 'organization', 'organization_id', 'user', 'user_id', 'resource_type', 'resource_id', 'action', 'created_at']
        read_only_fields = ['organization', 'user', 'created_at']

    def create(self, validated_data):
        return AccessLog.objects.create(
            organization_id=validated_data['organization_id'],
            user_id=validated_data.get('user_id'),
            resource_type=validated_data['resource_type'],
            resource_id=validated_data['resource_id'],
            action=validated_data['action'],
        )
