from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument, RetrievalQuery


class KnowledgeBaseSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'organization', 'organization_id', 'name', 'description', 'created_by', 'created_at']
        read_only_fields = ['organization', 'created_by', 'created_at']

    def create(self, validated_data):
        return KnowledgeBase.objects.create(
            organization_id=validated_data['organization_id'],
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            created_by=self.context['request'].user,
        )


class KnowledgeDocumentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    knowledge_base_id = serializers.UUIDField(write_only=True)
    document_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'knowledge_base_id': KnowledgeBase, 'document_id': Document}

    class Meta:
        model = KnowledgeDocument
        fields = ['id', 'organization', 'organization_id', 'knowledge_base', 'knowledge_base_id', 'document', 'document_id', 'title', 'status', 'created_at']
        read_only_fields = ['organization', 'knowledge_base', 'document', 'created_at']

    def create(self, validated_data):
        return KnowledgeDocument.objects.create(
            organization_id=validated_data['organization_id'],
            knowledge_base_id=validated_data['knowledge_base_id'],
            document_id=validated_data.get('document_id'),
            title=validated_data['title'],
            status=validated_data.get('status', 'pending'),
        )


class DocumentChunkSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    knowledge_document_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'knowledge_document_id': KnowledgeDocument}

    class Meta:
        model = DocumentChunk
        fields = ['id', 'organization', 'organization_id', 'knowledge_document', 'knowledge_document_id', 'chunk_index', 'content', 'created_at']
        read_only_fields = ['organization', 'knowledge_document', 'created_at']

    def create(self, validated_data):
        return DocumentChunk.objects.create(
            organization_id=validated_data['organization_id'],
            knowledge_document_id=validated_data['knowledge_document_id'],
            chunk_index=validated_data.get('chunk_index', 0),
            content=validated_data['content'],
        )


class RetrievalQuerySerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    knowledge_base_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'knowledge_base_id': KnowledgeBase}

    class Meta:
        model = RetrievalQuery
        fields = ['id', 'organization', 'organization_id', 'knowledge_base', 'knowledge_base_id', 'user', 'query', 'status', 'created_at']
        read_only_fields = ['organization', 'knowledge_base', 'user', 'status', 'created_at']

    def create(self, validated_data):
        return RetrievalQuery.objects.create(
            organization_id=validated_data['organization_id'],
            knowledge_base_id=validated_data['knowledge_base_id'],
            user=self.context['request'].user,
            query=validated_data['query'],
            status='not_implemented',
        )
