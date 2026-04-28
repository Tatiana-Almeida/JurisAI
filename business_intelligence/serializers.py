from rest_framework import serializers

from business_intelligence.models import MetricSnapshot, ReportDefinition, SavedReport
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class ReportDefinitionSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = ReportDefinition
        fields = ['id', 'organization', 'organization_id', 'name', 'slug', 'config', 'created_at']
        read_only_fields = ['organization', 'created_at']

    def create(self, validated_data):
        return ReportDefinition.objects.create(
            organization_id=validated_data['organization_id'],
            name=validated_data['name'],
            slug=validated_data['slug'],
            config=validated_data.get('config', {}),
        )


class SavedReportSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    report_definition_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'report_definition_id': ReportDefinition}

    class Meta:
        model = SavedReport
        fields = [
            'id', 'organization', 'organization_id', 'report_definition', 'report_definition_id',
            'saved_by', 'parameters', 'created_at',
        ]
        read_only_fields = ['organization', 'report_definition', 'saved_by', 'created_at']

    def create(self, validated_data):
        return SavedReport.objects.create(
            organization_id=validated_data['organization_id'],
            report_definition_id=validated_data['report_definition_id'],
            saved_by=self.context['request'].user,
            parameters=validated_data.get('parameters', {}),
        )


class MetricSnapshotSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = MetricSnapshot
        fields = ['id', 'organization', 'organization_id', 'metric_key', 'metric_value', 'captured_at', 'created_at']
        read_only_fields = ['organization', 'created_at']

    def create(self, validated_data):
        return MetricSnapshot.objects.create(
            organization_id=validated_data['organization_id'],
            metric_key=validated_data['metric_key'],
            metric_value=validated_data['metric_value'],
            captured_at=validated_data['captured_at'],
        )
