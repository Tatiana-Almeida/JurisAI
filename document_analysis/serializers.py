from rest_framework import serializers

from document_analysis.models import (
    DeadlineExtractionRun,
    DocumentComparison,
    DocumentDifference,
    ExtractedDeadlineSuggestion,
)
from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


class DocumentComparisonSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    left_document_id = serializers.UUIDField(write_only=True)
    right_document_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'left_document_id': Document, 'right_document_id': Document}

    class Meta:
        model = DocumentComparison
        fields = [
            'id', 'organization', 'organization_id', 'left_document', 'left_document_id',
            'right_document', 'right_document_id', 'requested_by', 'status', 'created_at',
        ]
        read_only_fields = ['organization', 'left_document', 'right_document', 'requested_by', 'status', 'created_at']

    def create(self, validated_data):
        return DocumentComparison.objects.create(
            organization_id=validated_data['organization_id'],
            left_document_id=validated_data['left_document_id'],
            right_document_id=validated_data['right_document_id'],
            requested_by=self.context['request'].user,
            status='pending',
        )


class DocumentDifferenceSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    comparison_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'comparison_id': DocumentComparison}

    class Meta:
        model = DocumentDifference
        fields = ['id', 'organization', 'organization_id', 'comparison', 'comparison_id', 'difference_type', 'content', 'created_at']
        read_only_fields = ['organization', 'comparison', 'created_at']

    def create(self, validated_data):
        return DocumentDifference.objects.create(
            organization_id=validated_data['organization_id'],
            comparison_id=validated_data['comparison_id'],
            difference_type=validated_data['difference_type'],
            content=validated_data['content'],
        )


class DeadlineExtractionRunSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    document_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'document_id': Document}

    class Meta:
        model = DeadlineExtractionRun
        fields = ['id', 'organization', 'organization_id', 'document', 'document_id', 'requested_by', 'status', 'created_at']
        read_only_fields = ['organization', 'document', 'requested_by', 'status', 'created_at']

    def create(self, validated_data):
        return DeadlineExtractionRun.objects.create(
            organization_id=validated_data['organization_id'],
            document_id=validated_data['document_id'],
            requested_by=self.context['request'].user,
            status='pending',
        )


class ExtractedDeadlineSuggestionSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    extraction_run_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'extraction_run_id': DeadlineExtractionRun}

    class Meta:
        model = ExtractedDeadlineSuggestion
        fields = [
            'id', 'organization', 'organization_id', 'extraction_run', 'extraction_run_id',
            'suggested_date', 'description', 'confidence', 'created_at',
        ]
        read_only_fields = ['organization', 'extraction_run', 'created_at']

    def create(self, validated_data):
        return ExtractedDeadlineSuggestion.objects.create(
            organization_id=validated_data['organization_id'],
            extraction_run_id=validated_data['extraction_run_id'],
            suggested_date=validated_data.get('suggested_date'),
            description=validated_data.get('description', ''),
            confidence=validated_data.get('confidence', 0),
        )
