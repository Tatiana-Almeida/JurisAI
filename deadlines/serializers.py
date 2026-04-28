from django.utils import timezone
from rest_framework import serializers
from deadlines.models import Deadline
from law_cases.models import LawCase
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class DeadlineSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    law_case_id = serializers.UUIDField(write_only=True)
    organization_id = serializers.UUIDField(write_only=True, required=False)
    days_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    tenant_relation_fields = {
        'law_case_id': LawCase,
    }

    class Meta:
        model = Deadline
        fields = ['id', 'law_case', 'law_case_id', 'due_date', 'completed', 'organization_id', 'created_at', 'updated_at', 'days_remaining', 'is_overdue']
        read_only_fields = ['law_case', 'created_at', 'updated_at', 'days_remaining', 'is_overdue']

    def create(self, validated_data, **kwargs):
        return Deadline.objects.create(
            law_case_id=validated_data['law_case_id'],
            due_date=validated_data['due_date'],
            completed=validated_data.get('completed', False),
            organization_id=validated_data['organization_id'],
        )

    def get_days_remaining(self, obj):
        delta = obj.due_date - timezone.now()
        return max(delta.days, 0)

    def get_is_overdue(self, obj):
        return obj.due_date < timezone.now()
