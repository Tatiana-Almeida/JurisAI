from rest_framework import serializers
from law_cases.models import LawCase
from accounts.serializers import UserSerializer
from accounts.models import User
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class LawCaseSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    lawyer = UserSerializer(read_only=True)
    client_id = serializers.UUIDField(write_only=True)
    lawyer_id = serializers.UUIDField(write_only=True)
    organization_id = serializers.UUIDField(write_only=True, required=False)
    tenant_relation_fields = {
        'client_id': User,
        'lawyer_id': User,
    }

    class Meta:
        model = LawCase
        fields = ['id', 'title', 'description', 'client', 'lawyer', 'client_id', 'lawyer_id', 'status', 'organization_id', 'created_at', 'updated_at', 'deleted']
        read_only_fields = ['deleted']

    def create(self, validated_data, **kwargs):
        return LawCase.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            client_id=validated_data['client_id'],
            lawyer_id=validated_data['lawyer_id'],
            organization_id=validated_data['organization_id'],
            status=validated_data.get('status', 'open'),
        )

    def update(self, instance, validated_data):
        for attr in ['title', 'description', 'status']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id) if instance.organization_id else None
        return data
