from rest_framework import serializers

from accounts.models import User
from calendar_events.models import CalendarEvent
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from law_cases.models import LawCase


class CalendarEventSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    law_case_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assigned_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    created_by_id = serializers.UUIDField(source='created_by.id', read_only=True)
    tenant_relation_fields = {
        'law_case_id': LawCase,
        'assigned_to_id': User,
    }

    class Meta:
        model = CalendarEvent
        fields = [
            'id', 'organization', 'organization_id', 'law_case', 'law_case_id', 'title', 'description',
            'event_type', 'start_at', 'end_at', 'location', 'created_by', 'created_by_id',
            'assigned_to', 'assigned_to_id', 'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['organization', 'law_case', 'created_by', 'assigned_to', 'created_at', 'updated_at']

    def create(self, validated_data):
        return CalendarEvent.objects.create(
            organization_id=validated_data['organization_id'],
            law_case_id=validated_data.get('law_case_id'),
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            event_type=validated_data.get('event_type', 'custom'),
            start_at=validated_data['start_at'],
            end_at=validated_data['end_at'],
            location=validated_data.get('location', ''),
            created_by=self.context['request'].user,
            assigned_to_id=validated_data.get('assigned_to_id'),
            status=validated_data.get('status', 'scheduled'),
        )

    def update(self, instance, validated_data):
        for field in ['title', 'description', 'event_type', 'start_at', 'end_at', 'location', 'status']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        if 'law_case_id' in validated_data:
            instance.law_case_id = validated_data['law_case_id']
        if 'assigned_to_id' in validated_data:
            instance.assigned_to_id = validated_data['assigned_to_id']
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization_id'] = str(instance.organization_id)
        data['law_case_id'] = str(instance.law_case_id) if instance.law_case_id else None
        data['assigned_to_id'] = str(instance.assigned_to_id) if instance.assigned_to_id else None
        data['created_by_id'] = str(instance.created_by_id)
        return data
