from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from ocr.models import OCRJob, OCRResult


class OCRJobSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(source='organization_id', read_only=True)
    document = serializers.UUIDField(source='document_id', read_only=True)
    requested_by = serializers.UUIDField(source='requested_by_id', read_only=True)

    class Meta:
        model = OCRJob
        fields = [
            'id',
            'organization',
            'document',
            'requested_by',
            'status',
            'extraction_method',
            'started_at',
            'finished_at',
            'error_message',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class OCRResultSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(source='organization_id', read_only=True)
    job = serializers.UUIDField(source='job_id', read_only=True)
    job_id = serializers.UUIDField(read_only=True)
    document = serializers.UUIDField(source='document_id', read_only=True)
    document_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = OCRResult
        fields = [
            'id',
            'organization',
            'job',
            'job_id',
            'document',
            'document_id',
            'extracted_text',
            'char_count',
            'metadata',
            'created_at',
        ]
        read_only_fields = fields


class RunOCRSerializer(TenantRelationValidationMixin, serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    update_document_content = serializers.BooleanField(required=False, default=False)
    tenant_relation_fields = {'document_id': Document}

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'document_id': 'Organizacao atual nao encontrada.'})

        document_id = data.get('document_id') or self.context.get('document_id')
        data['document_id'] = document_id
        data['organization_id'] = str(organization.id)
        return self.validate_tenant_relations(data)


class ApplyOCRResultSerializer(TenantRelationValidationMixin, serializers.Serializer):
    result_id = serializers.UUIDField(required=False)
    tenant_relation_fields = {'result_id': OCRResult}

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'result_id': 'Organizacao atual nao encontrada.'})

        result_id = data.get('result_id') or self.context.get('result_id')
        data['result_id'] = result_id
        data['organization_id'] = str(organization.id)
        return self.validate_tenant_relations(data)
