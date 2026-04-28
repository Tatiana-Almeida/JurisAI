from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from ocr.models import OCRJob, OCRResult


class OCRJobSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    document_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'document_id': Document}

    class Meta:
        model = OCRJob
        fields = ['id', 'organization', 'organization_id', 'document', 'document_id', 'requested_by', 'status', 'created_at']
        read_only_fields = ['organization', 'document', 'requested_by', 'status', 'created_at']

    def create(self, validated_data):
        return OCRJob.objects.create(
            organization_id=validated_data['organization_id'],
            document_id=validated_data.get('document_id'),
            requested_by=self.context['request'].user,
            status='pending',
        )


class OCRResultSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    job_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'job_id': OCRJob}

    class Meta:
        model = OCRResult
        fields = ['id', 'organization', 'organization_id', 'job', 'job_id', 'extracted_text', 'confidence', 'created_at']
        read_only_fields = ['organization', 'job', 'created_at']

    def create(self, validated_data):
        return OCRResult.objects.create(
            organization_id=validated_data['organization_id'],
            job_id=validated_data['job_id'],
            extracted_text=validated_data.get('extracted_text', ''),
            confidence=validated_data.get('confidence', 0),
        )
