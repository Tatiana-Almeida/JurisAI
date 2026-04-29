from django.contrib import admin

from knowledge_base.models import ChunkEmbedding, DocumentChunk, IndexingJob, KnowledgeBase, KnowledgeDocument, RetrievalQuery


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'is_active', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'organization')


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'knowledge_base', 'source_type', 'status', 'indexed_at')
    search_fields = ('title', 'error_message')
    list_filter = ('source_type', 'status', 'organization')


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('knowledge_document', 'organization', 'chunk_index', 'char_count', 'embedding_status', 'created_at')
    search_fields = ('content',)
    list_filter = ('organization',)


@admin.register(RetrievalQuery)
class RetrievalQueryAdmin(admin.ModelAdmin):
    list_display = ('organization', 'knowledge_base', 'created_by', 'status', 'created_at')
    search_fields = ('query', 'answer')
    list_filter = ('status', 'organization')


@admin.register(IndexingJob)
class IndexingJobAdmin(admin.ModelAdmin):
    list_display = ('knowledge_base', 'document', 'status', 'chunks_created', 'chunks_deleted', 'created_at')
    search_fields = ('error_message',)
    list_filter = ('status', 'organization')


@admin.register(ChunkEmbedding)
class ChunkEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('chunk', 'organization', 'provider', 'model', 'status', 'created_at')
    search_fields = ('provider', 'model', 'error_message')
    list_filter = ('status', 'organization')
