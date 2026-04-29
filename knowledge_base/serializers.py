from rest_framework import serializers

from documents.models import Document
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin
from knowledge_base.models import (
    ChunkEmbedding,
    DocumentChunk,
    EmbeddingAuditLog,
    IndexingJob,
    KnowledgeBase,
    KnowledgeDocument,
    RAGSettings,
    RetrievalQuery,
)
from knowledge_base.services import validate_embedding_policy


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


class ChunkEmbeddingSerializer(
    TenantRelationValidationMixin,
    OrganizationScopedValidationMixin,
    serializers.ModelSerializer,
):
    organization_id = serializers.UUIDField(write_only=True, required=False)
    chunk_id = serializers.UUIDField(write_only=True)
    tenant_relation_fields = {'chunk_id': DocumentChunk}

    class Meta:
        model = ChunkEmbedding
        fields = [
            'id',
            'organization',
            'organization_id',
            'chunk',
            'chunk_id',
            'provider',
            'model',
            'vector',
            'status',
            'error_message',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['organization', 'chunk', 'created_at', 'updated_at']

    def create(self, validated_data):
        return ChunkEmbedding.objects.create(
            organization_id=validated_data['organization_id'],
            chunk_id=validated_data['chunk_id'],
            provider=validated_data.get('provider', ''),
            model=validated_data.get('model', ''),
            vector=validated_data.get('vector'),
            status=validated_data.get('status', 'not_generated'),
            error_message=validated_data.get('error_message', ''),
        )


class DocumentChunkSerializer(serializers.ModelSerializer):
    knowledge_document_id = serializers.UUIDField(source='knowledge_document_id', read_only=True)
    document_id = serializers.UUIDField(source='document_id', read_only=True, allow_null=True)
    embedding = ChunkEmbeddingSerializer(read_only=True)

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
            'embedding_status',
            'embedding',
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
            'retrieval_method',
            'confidence',
            'sources_count',
            'sources_payload',
            'created_at',
        ]
        read_only_fields = fields


class RAGSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAGSettings
        fields = [
            'organization',
            'retrieval_mode',
            'external_embeddings_enabled',
            'embedding_provider',
            'embedding_model',
            'require_human_review_for_ai_answers',
            'allow_document_content_to_external_provider',
            'max_sources_per_answer',
            'min_confidence_threshold',
            'updated_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['organization', 'updated_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        instance = self.instance
        candidate = RAGSettings(
            organization=getattr(instance, 'organization', None),
            retrieval_mode=attrs.get('retrieval_mode', getattr(instance, 'retrieval_mode', 'textual')),
            external_embeddings_enabled=attrs.get(
                'external_embeddings_enabled',
                getattr(instance, 'external_embeddings_enabled', False),
            ),
            embedding_provider=attrs.get('embedding_provider', getattr(instance, 'embedding_provider', '')),
            embedding_model=attrs.get('embedding_model', getattr(instance, 'embedding_model', '')),
            require_human_review_for_ai_answers=attrs.get(
                'require_human_review_for_ai_answers',
                getattr(instance, 'require_human_review_for_ai_answers', True),
            ),
            allow_document_content_to_external_provider=attrs.get(
                'allow_document_content_to_external_provider',
                getattr(instance, 'allow_document_content_to_external_provider', False),
            ),
            max_sources_per_answer=attrs.get(
                'max_sources_per_answer',
                getattr(instance, 'max_sources_per_answer', 5),
            ),
            min_confidence_threshold=attrs.get(
                'min_confidence_threshold',
                getattr(instance, 'min_confidence_threshold', 'low'),
            ),
        )
        errors = validate_embedding_policy(candidate)
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class EmbeddingAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddingAuditLog
        fields = [
            'id',
            'organization',
            'chunk',
            'knowledge_document',
            'provider',
            'model',
            'action',
            'status',
            'reason',
            'metadata',
            'created_by',
            'created_at',
        ]
        read_only_fields = fields


class IndexingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexingJob
        fields = [
            'id',
            'organization',
            'knowledge_base',
            'knowledge_document',
            'document',
            'status',
            'started_at',
            'finished_at',
            'chunks_created',
            'chunks_deleted',
            'error_message',
            'metadata',
            'created_by',
            'created_at',
            'updated_at',
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


class ReindexDocumentSerializer(IndexDocumentSerializer):
    pass


class PrepareEmbeddingsSerializer(TenantRelationValidationMixin, serializers.Serializer):
    knowledge_document_id = serializers.UUIDField(required=False)
    tenant_relation_fields = {'knowledge_document_id': KnowledgeDocument}

    def validate(self, data):
        organization = getattr(self.context['request'].user, 'organization', None)
        if organization is None:
            raise serializers.ValidationError({'knowledge_document_id': 'Organizacao atual nao encontrada.'})

        data['organization_id'] = str(organization.id)
        return self.validate_tenant_relations(data)


class KnowledgeSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    limit = serializers.IntegerField(required=False, min_value=1, max_value=10, default=5)


class KnowledgeAskSerializer(KnowledgeSearchSerializer):
    pass
