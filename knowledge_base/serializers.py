from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument, RetrievalQuery


class KnowledgeBaseSerializer(OrganizationScopedValidationMixin, serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = KnowledgeBase
        fields = [
            'id',
            'organization',
            'organization_id',
            'name',
            'description',
            'is_active',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['organization', 'created_by', 'created_at', 'updated_at']


class KnowledgeDocumentSerializer(
    TenantRelationValidationMixin,
    OrganizationScopedValidationMixin,
    serializers.ModelSerializer,
):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    knowledge_base_id = serializers.UUIDField(write_only=True)
    document_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tenant_relation_fields = {'knowledge_base_id': KnowledgeBase, 'document_id': Document}

    class Meta:
        model = KnowledgeDocument
        fields = [
            'id',
            'organization',
            'organization_id',
            'knowledge_base',
            'knowledge_base_id',
            'document',
            'document_id',
            'title',
            'source_type',
            'status',
            'indexed_at',
            'error_message',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'organization',
            'knowledge_base',
            'document',
            'status',
            'indexed_at',
            'error_message',
            'created_by',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        return KnowledgeDocument.objects.create(
            organization_id=validated_data['organization_id'],
            knowledge_base_id=validated_data['knowledge_base_id'],
            document_id=validated_data.get('document_id'),
            title=validated_data['title'],
            source_type=validated_data.get('source_type', 'manual'),
            created_by=validated_data.get('created_by', self.context['request'].user),
        )


class DocumentChunkSerializer(serializers.ModelSerializer):
    knowledge_document_id = serializers.UUIDField(source='knowledge_document_id', read_only=True)
    document_id = serializers.UUIDField(source='document_id', read_only=True, allow_null=True)

    class Meta:
        model = DocumentChunk
        fields = [
            'id',
            'organization',
            'knowledge_document_id',
            'document_id',
            'chunk_index',
            'content',
            'content_hash',
            'metadata',
            'char_count',
            'created_at',
        ]
        read_only_fields = fields


class RetrievalQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetrievalQuery
        fields = [
            'id',
            'organization',
            'knowledge_base',
            'created_by',
            'query',
            'answer',
            'status',
            'sources_payload',
            'created_at',
        ]
        read_only_fields = fields


class IndexDocumentSerializer(TenantRelationValidationMixin, serializers.Serializer):
    document_id = serializers.UUIDField()
    tenant_relation_fields = {'document_id': Document}

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'document_id': 'Organizacao atual nao encontrada.'})

        data['organization_id'] = str(organization.id)
        return self.validate_tenant_relations(data)


class KnowledgeSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    limit = serializers.IntegerField(required=False, min_value=1, max_value=10, default=5)


class KnowledgeAskSerializer(KnowledgeSearchSerializer):
    pass
