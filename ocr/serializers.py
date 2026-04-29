from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from knowledge_base.models import KnowledgeBase
from ocr.models import (
    OCRAuditLog,
    OCRJob,
    OCRKnowledgeBasePipelineRun,
    OCRResult,
    OCRSettings,
)
from ocr.services import validate_ocr_provider_policy


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


class OCRKnowledgeBasePipelineRunSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(source='organization_id', read_only=True)
    document = serializers.UUIDField(source='document_id', read_only=True)
    knowledge_base = serializers.UUIDField(source='knowledge_base_id', read_only=True)
    ocr_job = serializers.UUIDField(source='ocr_job_id', read_only=True, allow_null=True)
    ocr_result = serializers.UUIDField(source='ocr_result_id', read_only=True, allow_null=True)
    knowledge_document = serializers.UUIDField(source='knowledge_document_id', read_only=True, allow_null=True)
    indexing_job = serializers.UUIDField(source='indexing_job_id', read_only=True, allow_null=True)
    created_by = serializers.UUIDField(source='created_by_id', read_only=True)

    class Meta:
        model = OCRKnowledgeBasePipelineRun
        fields = [
            'id',
            'organization',
            'document',
            'knowledge_base',
            'ocr_job',
            'ocr_result',
            'knowledge_document',
            'indexing_job',
            'status',
            'step',
            'update_document_content',
            'error_message',
            'metadata',
            'created_by',
            'started_at',
            'finished_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class RunOCRKnowledgeBasePipelineSerializer(TenantRelationValidationMixin, serializers.Serializer):
    document_id = serializers.UUIDField()
    knowledge_base_id = serializers.UUIDField()
    update_document_content = serializers.BooleanField(required=False, default=True)
    tenant_relation_fields = {
        'document_id': Document,
        'knowledge_base_id': KnowledgeBase,
    }

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'document_id': 'Organizacao atual nao encontrada.'})

        data['organization_id'] = str(organization.id)
        validated = self.validate_tenant_relations(data)
        if not validated.get('update_document_content', True):
            raise serializers.ValidationError(
                {'update_document_content': 'update_document_content must be true for OCR-to-KnowledgeBase pipeline.'}
            )
        return validated


class OCRSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRSettings
        fields = [
            'organization',
            'advanced_ocr_enabled',
            'external_ocr_enabled',
            'allow_document_content_to_external_ocr_provider',
            'preferred_ocr_provider',
            'preferred_ocr_model',
            'image_ocr_mode',
            'scanned_pdf_ocr_mode',
            'require_human_review',
            'updated_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['organization', 'updated_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        instance = self.instance
        candidate = OCRSettings(
            organization=getattr(instance, 'organization', None),
            advanced_ocr_enabled=attrs.get(
                'advanced_ocr_enabled',
                getattr(instance, 'advanced_ocr_enabled', False),
            ),
            external_ocr_enabled=attrs.get(
                'external_ocr_enabled',
                getattr(instance, 'external_ocr_enabled', False),
            ),
            allow_document_content_to_external_ocr_provider=attrs.get(
                'allow_document_content_to_external_ocr_provider',
                getattr(instance, 'allow_document_content_to_external_ocr_provider', False),
            ),
            preferred_ocr_provider=attrs.get(
                'preferred_ocr_provider',
                getattr(instance, 'preferred_ocr_provider', 'local'),
            ),
            preferred_ocr_model=attrs.get(
                'preferred_ocr_model',
                getattr(instance, 'preferred_ocr_model', ''),
            ),
            image_ocr_mode=attrs.get(
                'image_ocr_mode',
                getattr(instance, 'image_ocr_mode', 'disabled'),
            ),
            scanned_pdf_ocr_mode=attrs.get(
                'scanned_pdf_ocr_mode',
                getattr(instance, 'scanned_pdf_ocr_mode', 'disabled'),
            ),
            require_human_review=attrs.get(
                'require_human_review',
                getattr(instance, 'require_human_review', True),
            ),
        )
        errors = validate_ocr_provider_policy(candidate)
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class OCRAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRAuditLog
        fields = [
            'id',
            'organization',
            'document',
            'ocr_job',
            'action',
            'provider',
            'mode',
            'status',
            'reason',
            'metadata',
            'created_by',
            'created_at',
        ]
        read_only_fields = fields


class AdvancedOCRRunSerializer(TenantRelationValidationMixin, serializers.Serializer):
    document_id = serializers.UUIDField(required=False)
    mode = serializers.ChoiceField(required=False, default='auto', choices=['auto'])
    tenant_relation_fields = {'document_id': Document}

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'document_id': 'Organizacao atual nao encontrada.'})

        document_id = data.get('document_id') or self.context.get('document_id')
        data['document_id'] = document_id
        data['organization_id'] = str(organization.id)
        return self.validate_tenant_relations(data)
