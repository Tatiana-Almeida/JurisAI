from rest_framework import serializers

from accounts.models import User
from crm.models import Consultation, Lead, LeadActivity
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class LeadSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    owner_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'owner_id': User}

    class Meta:
        model = Lead
        fields = [
            'id', 'organization', 'organization_id', 'name', 'email', 'phone', 'source',
            'status', 'notes', 'owner', 'owner_id', 'created_at',
        ]
        read_only_fields = ['organization', 'owner', 'created_at']

    def create(self, validated_data):
        return Lead.objects.create(
            organization_id=validated_data['organization_id'],
            owner_id=validated_data.get('owner_id'),
            name=validated_data['name'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            source=validated_data.get('source', ''),
            status=validated_data.get('status', 'new'),
            notes=validated_data.get('notes', ''),
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['owner_id'] = str(instance.owner_id) if instance.owner_id else None
        return data


class LeadActivitySerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    lead_id = serializers.UUIDField(write_only=True)
    author_id = serializers.UUIDField(source='author.id', read_only=True)
    tenant_relation_fields = {'lead_id': Lead}

    class Meta:
        model = LeadActivity
        fields = [
            'id', 'organization', 'organization_id', 'lead', 'lead_id', 'author',
            'author_id', 'activity_type', 'description', 'created_at',
        ]
        read_only_fields = ['organization', 'lead', 'author', 'created_at']

    def create(self, validated_data):
        return LeadActivity.objects.create(
            organization_id=validated_data['organization_id'],
            lead_id=validated_data['lead_id'],
            author=self.context['request'].user,
            activity_type=validated_data.get('activity_type', 'note'),
            description=validated_data['description'],
        )


class ConsultationSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    lead_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assigned_to_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'lead_id': Lead, 'assigned_to_id': User}

    class Meta:
        model = Consultation
        fields = [
            'id', 'organization', 'organization_id', 'lead', 'lead_id', 'assigned_to',
            'assigned_to_id', 'scheduled_for', 'notes', 'status', 'created_at',
        ]
        read_only_fields = ['organization', 'lead', 'assigned_to', 'created_at']

    def create(self, validated_data):
        return Consultation.objects.create(
            organization_id=validated_data['organization_id'],
            lead_id=validated_data.get('lead_id'),
            assigned_to_id=validated_data['assigned_to_id'],
            scheduled_for=validated_data['scheduled_for'],
            notes=validated_data.get('notes', ''),
            status=validated_data.get('status', 'scheduled'),
        )
